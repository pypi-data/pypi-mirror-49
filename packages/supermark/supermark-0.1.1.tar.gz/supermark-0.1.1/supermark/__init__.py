from enum import Enum
import os
import yaml
import pypandoc

import random
import string
import re

import hashlib

shake = hashlib.shake_128()

ENV_PATTERN = re.compile('[a-zA-Z]*:')

def random_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

from colorama import init, Fore, Style
init(autoreset=True)

def tell(message, level='info', chunk=None):
    # Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    # Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    # Style: DIM, NORMAL, BRIGHT, RESET_ALL
    if chunk is not None:
        message = '{} line {}: {}'.format(chunk.path, chunk.start_line_number, message)
    if level == 'info':
        print(Fore.GREEN + Style.BRIGHT +  ' - ' + Style.RESET_ALL + message)
    elif level == 'warn':
        print(Fore.YELLOW + Style.BRIGHT +  ' - ' + Style.RESET_ALL + message)
    else:
        print(Fore.RED + Style.BRIGHT +  ' - ' + Style.NORMAL + message)


class ParserState(Enum):
    MARKDOWN = 0
    YAML = 1
    CODE = 2
    HTML = 3

def is_empty(s_line):
    return not s_line

class RawChunk:

    def __init__(self, lines, chunk_type, start_line_number, path):
        self.lines = lines
        self.type = chunk_type
        self.start_line_number = start_line_number
        self.path = path
        # check if we only got empty lines
        def all_empty(lines):
            if len(lines) == 0: return True
            for line in lines:
                if line.strip(): return False
            return True
        self._is_empty = all_empty(self.lines)
        # remove blank lines from the beginning
        while (len(self.lines)>0 and is_empty(self.lines[0].strip())):
            self.lines.pop(0)
            self.start_line_number = self.start_line_number + 1
    
    def is_empty(self):
        return self._is_empty

    def get_type(self):
        return self.type

    def get_first_line(self):
        if len(self.lines) == 0:
            return 'empty'
        return self.lines[0]

def yaml_start(s_line):
    return s_line == '---'

def yaml_stop(s_line):
    return s_line == '---'

def markdown_start(s_line, empty_lines):
    return s_line.startswith('# ') or empty_lines >= 2 or s_line.startswith('Aside:')

def html_start(s_line, empty_lines):
    return s_line.startswith('<') and empty_lines >= 2

def html_stop(empty_lines):
    return empty_lines >= 2

def code_start(s_line):
    return s_line.startswith('```')

def code_stop(s_line):
    return s_line.startswith('```')

def _parse(lines, path):
    chunks = []
    current_lines = []
    empty_lines = 0
    state = ParserState.MARKDOWN
    start_line_number = 0

    for line_number, line in enumerate(lines, start=1):
        s_line = line.strip()
        if state==ParserState.MARKDOWN:
            if is_empty(s_line):
                empty_lines = empty_lines + 1
                current_lines.append(line)
            elif yaml_start(s_line):
                chunks.append(RawChunk(current_lines, ParserState.MARKDOWN, start_line_number, path))
                state = ParserState.YAML
                current_lines = []
                start_line_number = line_number
                empty_lines = 0
            elif code_start(s_line):
                chunks.append(RawChunk(current_lines, ParserState.MARKDOWN, start_line_number, path))
                state = ParserState.CODE
                current_lines = [line]
                start_line_number = line_number
                empty_lines = 0
            elif html_start(s_line, empty_lines):
                chunks.append(RawChunk(current_lines, ParserState.MARKDOWN, start_line_number, path))
                state = ParserState.HTML
                current_lines = []
                current_lines.append(line)
                start_line_number = line_number
                empty_lines = 0
            elif markdown_start(s_line, empty_lines):
                chunks.append(RawChunk(current_lines, ParserState.MARKDOWN, start_line_number, path))
                state = ParserState.MARKDOWN
                current_lines = []
                current_lines.append(line)
                start_line_number = line_number
                empty_lines = 0
            else:
                current_lines.append(line)
                empty_lines = 0
        elif state==ParserState.YAML:
            if yaml_stop(s_line):
                chunks.append(RawChunk(current_lines, ParserState.YAML, start_line_number, path))
                state = ParserState.MARKDOWN
                current_lines = []
                start_line_number = line_number + 1
            else:
                current_lines.append(line)
        elif state==ParserState.CODE:
            if code_stop(s_line):
                current_lines.append(line)
                chunks.append(RawChunk(current_lines, ParserState.CODE, start_line_number, path))
                state = ParserState.MARKDOWN
                current_lines = []
                start_line_number = line_number + 1
            else:
                current_lines.append(line)
        elif state==ParserState.HTML:
            if is_empty(s_line):
                empty_lines = empty_lines + 1
                current_lines.append(line)
            elif html_stop(empty_lines):
                chunks.append(RawChunk(current_lines, ParserState.HTML, start_line_number, path))
                state = ParserState.MARKDOWN
                current_lines = []
                current_lines.append(line)
                start_line_number = line_number
                empty_lines = 0
            else:
                current_lines.append(line)
                empty_lines = 0
    # create last chunk
    chunks.append(RawChunk(current_lines, state, start_line_number, path))
    # remove chunks that turn out to be empty
    chunks = [item for item in chunks if not item.is_empty()]
    return chunks

class Chunk:

    def __init__(self, raw_chunk, page_variables):
        self.raw_chunk = raw_chunk
        self.page_variables = page_variables
        self.aside = False
        self.asides = []

    def is_aside(self):
        return self.aside

    def get_asides(self):
        return self.asides

    def get_first_line(self):
        return self.raw_chunk.lines[0]

    def get_type(self):
        return self.raw_chunk.type
    
    def get_start_line_number(self):
        return self.raw_chunk.start_line_number

    def get_content(self):
        return ''.join(self.raw_chunk.lines)


class YAMLChunk(Chunk):

     def __init__(self, raw_chunk, dictionary, page_variables, required=None, optional=None):
          super().__init__(raw_chunk, page_variables)
          self.dictionary = dictionary
          required = required or []
          optional = optional or []
          for key in required:
               if key not in self.dictionary:
                    tell("YAML section misses required parameter '{}'.".format(key), level='error', chunk=raw_chunk)
          for key in self.dictionary.keys():
               if (key not in required) and (key not in optional) and (key != 'type'):
                    tell("YAML section has unknown parameter '{}'.".format(key), level='warn', chunk=raw_chunk)


class YAMLVideoChunk(YAMLChunk):

    def __init__(self, raw_chunk, dictionary, page_variables):
        super().__init__(raw_chunk, dictionary, page_variables, required=['video'], optional=['start', 'caption'])
    
    def to_html(self):
        html = []
        html.append('<div class="figure">')
        start = ''
        if 'start' in self.dictionary:
            start = '?start={}'.format(self.dictionary['start'])
        width = 560
        height = 315
        video = self.dictionary['video']
        html.append('<iframe width="{}" height="{}" src="https://www.youtube.com/embed/{}{}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'.format(width, height, video, start))
        if 'caption' in self.dictionary:
            html.append('<span name="{}">&nbsp;</span>'.format(self.dictionary['video']))
            html_caption = pypandoc.convert_text(self.dictionary['caption'], 'html', format='md')
            html.append('<aside name="{}"><p>{}</p></aside>'.format(self.dictionary['video'], html_caption))
        html.append('</div>')
        return '\n'.join(html)


class YAMLFigureChunk(YAMLChunk):

    def __init__(self, raw_chunk, dictionary, page_variables):
        super().__init__(raw_chunk, dictionary, page_variables, required=['source'], optional=['caption'])

    def to_html(self):
        html = []
        html.append('<div class="figure">')
        if 'source' not in self.dictionary:
            print('source attribute missing!')
            print(''.join(self.raw_chunk.lines))
        else:
            if 'caption' in self.dictionary:
                html.append('<img src="{}" alt="{}" width="100%"/>'.format(self.dictionary['source'], self.dictionary['caption']))
                html.append('<span name="{}">&nbsp;</span>'.format(self.dictionary['source']))
                html_caption = pypandoc.convert_text(self.dictionary['caption'], 'html', format='md')
                html.append('<aside name="{}"><p>{}</p></aside>'.format(self.dictionary['source'], html_caption))
            else:
                html.append('<img src="{}" width="100%"/>'.format(self.dictionary['source']))
        html.append('</div>')
        return '\n'.join(html)

class YAMLButtonChunk(YAMLChunk):

    def __init__(self, raw_chunk, dictionary, page_variables):
        super().__init__(raw_chunk, dictionary, page_variables, required=['url', 'text'])

    def to_html(self):
        clazz = 'ntnu-button'
        html = []
        html.append('<a class="{}" href="{}">{}</a>'.format(clazz, self.dictionary['url'], self.dictionary['text']))
        return '\n'.join(html)


class YAMLDataChunk(YAMLChunk):

    def __init__(self, raw_chunk, dictionary, page_variables):
        super().__init__(raw_chunk, dictionary, page_variables, optional=['status'])


class MarkdownChunk(Chunk):

    def __init__(self, raw_chunk, page_variables):
        super().__init__(raw_chunk, page_variables)
        self.aside = super().get_first_line().strip().startswith('Aside:')
        self.is_section = super().get_first_line().startswith('# ')
    
    def to_html(self):
        if self.aside:
            content = self.get_content()[6:].strip() # remove 'aside: '
            #aside_id = random_id()
            shake.update(content.encode('utf-8'))
            aside_id = shake.hexdigest(3)
            output = []
            output.append('<span name="{}"></span><aside name="{}">'.format(aside_id, aside_id))
            output.append(pypandoc.convert_text(content, 'html', format='md'))
            output.append('</aside>')
            return ''.join(output)
        else:
            extra_args = ['--highlight-style', 'pygments']
            output = pypandoc.convert_text(self.get_content(), 'html', format='md', extra_args=extra_args)
            return output


class HTMLChunk(Chunk):

    def __init__(self, raw_chunk, page_variables):
        super().__init__(raw_chunk, page_variables)
    
    def to_html(self):
        return super().get_content()


class CodeChunk(Chunk):

    def __init__(self, raw_chunk, page_variables):
        super().__init__(raw_chunk, page_variables)

    def to_html(self):
        extra_args = ['--highlight-style', 'pygments']
        output = pypandoc.convert_text(self.get_content(), 'html', format='md', extra_args=extra_args)
        return output


def cast(rawchunks):
    chunks = []
    page_variables = {}
    for raw in rawchunks:
        chunk_type = raw.get_type()
        if chunk_type==ParserState.MARKDOWN:
            chunks.append(MarkdownChunk(raw, page_variables))
        elif chunk_type==ParserState.YAML:
            dictionary = yaml.safe_load(''.join(raw.lines))
            if isinstance(dictionary, dict):
                if 'type' in dictionary:
                    yaml_type = dictionary['type']
                    if yaml_type == 'youtube':
                        chunks.append(YAMLVideoChunk(raw, dictionary, page_variables))
                    elif yaml_type == 'figure':
                        chunks.append(YAMLFigureChunk(raw, dictionary, page_variables))
                    elif yaml_type == 'button':
                        chunks.append(YAMLButtonChunk(raw, dictionary, page_variables))
                    # TODO warn if unknown type
                else:
                    data_chunk = YAMLDataChunk(raw, dictionary, page_variables)
                    try:
                        page_variables.update(data_chunk.dictionary)
                    except ValueError as e:
                        print(e)
                    chunks.append(data_chunk)
            else:
                tell('Something is wrong with the YAML section.', level='error', chunk=raw)
        elif chunk_type==ParserState.HTML:
            chunks.append(HTMLChunk(raw, page_variables))
        elif chunk_type==ParserState.CODE:
            chunks.append(CodeChunk(raw, page_variables))
    return chunks

def arrange_assides(chunks):
    main_chunks = []
    current_main_chunk = None
    for chunk in chunks:
        if chunk.is_aside():
            if current_main_chunk is not None:
                current_main_chunk.asides.append(chunk)
            else:
                tell('Aside chunk cannot be defined as first element.')
                main_chunks.append(chunk)
        else:
            main_chunks.append(chunk)
            current_main_chunk = chunk
    return main_chunks

def transform_page_to_html(lines, template, filepath, abort_draft):
    chunks = _parse(lines, filepath)
    chunks = cast(chunks)
    chunks = arrange_assides(chunks)

    content = []
    content.append('<div class="page">')
    if len(chunks)==0:
        pass
    else:
        first_chunk = chunks[0]
        if isinstance(first_chunk, MarkdownChunk) and not first_chunk.is_section:
            content.append('    <section class="content">')
    
    for chunk in chunks:
        if 'status' in chunk.page_variables and abort_draft and chunk.page_variables['status'] == 'draft':
            content.append('<mark>This site is under construction.</mark>')
            break
        if isinstance(chunk, YAMLDataChunk):
            pass
        elif isinstance(chunk, MarkdownChunk):
            if chunk.is_section:
                # open a new section
                content.append('    </section>')
                content.append('    <section class="content">')
            for aside in chunk.asides:
                content.append(aside.to_html())
            content.append(chunk.to_html())
        else:
            for aside in chunk.asides:
                content.append(aside.to_html())
            content.append(chunk.to_html())

    content.append('    </section>')
    content.append('</div>')
    content = '\n'.join(content)
    parameters = {'content': content}
    html = template.format(**parameters)
    return html

def _create_target(source_file_path, target_file_path, template_file_path, overwrite):
    if not os.path.isfile(target_file_path):
        return True
    if overwrite:
        return True
    if not os.path.isfile(template_file_path):
        return os.path.getmtime(target_file_path) < os.path.getmtime(source_file_path)
    else:
        return os.path.getmtime(target_file_path) < os.path.getmtime(source_file_path) and os.path.getmtime(target_file_path) < os.path.getmtime(template_file_path)

def write_file(html, target_file_path):
    try:# latin-1
        with open(target_file_path, "w", encoding='latin-1') as html_file:
            html_file.write(html)
            print('latin-1: {}'.format(target_file_path))
    except UnicodeEncodeError as error:
        print(error)
    with open(target_file_path, "w", encoding='utf-8') as html_file:
        html_file.write(html)

def process_file(source_file_path, target_file_path, template, abort_draft):
        #print(source_file_path)
        with open(source_file_path, 'r', encoding='latin-1') as file:
            lines = file.readlines()
            html = transform_page_to_html(lines, template, source_file_path, abort_draft)
            write_file(html, target_file_path)

def default_html_template():
    html = []
    html.append('<head><title></title></head>')
    html.append('<body>')
    html.append('{content}')
    html.append('</body>')
    html.append('</html>')
    return '\n'.join(html)

def load_html_template(template_path):
    try:
        with open(template_path, 'r', encoding='utf-8', errors="surrogateescape") as templatefile:
            template = templatefile.read()
            return template
    except FileNotFoundError as error:
        tell('Template file missing. Expected at {}. Using default template.'.format(template_path))
        return default_html_template()

def build(input_path, output_path, template_file, rebuild_all_pages = True, abort_draft = True):
    template = load_html_template(template_file)
    for filename in os.listdir(input_path):
        source_file_path = os.path.join(input_path, filename)
        if os.path.isfile(source_file_path) and filename.endswith('.md'):
            target_file_name = os.path.splitext(os.path.basename(filename))[0] + '.html'
            target_file_path = os.path.join(output_path, target_file_name)
            if _create_target(source_file_path, target_file_path, template_file, rebuild_all_pages):
                process_file(source_file_path, target_file_path, template, abort_draft)