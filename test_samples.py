import asyncio
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import List
from urllib import parse

import mistune

MAX_TASKS = 3


@dataclass(frozen=True)
class CodeBlock:
    language: str
    code: str
    location: Path


@dataclass(frozen=True)
class TestOutcome:
    block: CodeBlock
    stdout: str
    returncode: int


def get_top_level_block_codes(mark: str, location: Path) -> List[CodeBlock]:
    markdown = mistune.create_markdown(renderer=mistune.AstRenderer())
    ast = markdown(mark)

    named_blocks = defaultdict(list)
    unnamed_blocks = []
    for elt in ast:
        if elt.get('type') == 'block_code':
            # N.B. mistune 2.0.0a5 creates an `info` key with value None if the
            #      info parameter doesn't exist. Thus we can't use `.get()` directly
            language = elt.get('info') or ''
            language = language.lower()

            language, _, options = language.partition('?')
            if options:
                name = parse.parse_qs(options).get('example', [''])[0]
                if name:
                    named_blocks[name].append(CodeBlock(code=elt.get('text'), language=language, location=location))
                else:
                    unnamed_blocks.append(CodeBlock(code=elt.get('text'), language=language, location=location))
            else:
                unnamed_blocks.append(CodeBlock(code=elt.get('text'), language=language, location=location))

    for block_of_blocks in named_blocks.values():
        unnamed_blocks.append(CodeBlock(
            code='\n\n'.join(block.code for block in block_of_blocks),
            language=block_of_blocks[0].language.split()[0].lower(),
            location=location
        ))

    return unnamed_blocks


def format_file(block: CodeBlock, prefix: str = 'Running') -> str:
    cleaned_code = re.sub(r'\s', ' ', block.code[:50])
    return f"{prefix} code in {block.location} that begins {cleaned_code}"


async def main():
    semaphore = asyncio.Semaphore(MAX_TASKS)

    async def run_docker(block: CodeBlock) -> TestOutcome:
        async with semaphore:
            print(format_file(block))
            process = await asyncio.create_subprocess_exec(
                'docker',
                'run',
                '--rm',
                'tester',
                'python',
                '-c',
                block.code,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT
            )
            stdout, _ = await process.communicate()

        return TestOutcome(
            block=block,
            stdout=stdout,
            returncode=process.returncode
        )

    async def create_tasks(blocks):
        tasks = [run_docker(block) for block in blocks]
        return await asyncio.gather(*tasks)

    all_blocks: List[CodeBlock] = []
    for filename in Path('Time_Series').glob('**/*.md'):
        with open(filename, 'rt') as infile:
            text = infile.read()
        blocks = get_top_level_block_codes(text, filename)
        all_blocks.extend(blocks)

    all_blocks = [block for block in all_blocks if block.language.startswith('py')]
    outputs = await create_tasks(all_blocks)
    for output in outputs:
        if output.returncode != 0:
            print()
            print(f"===== {format_file(output.block, prefix='Error in')} =====")
            print(output.stdout)
            print()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()