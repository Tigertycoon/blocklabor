"""Validate the published course graph, book references, pack lock and world boundary."""
from pathlib import Path
import json, tomllib
import nbtlib
from nbtlib.literal.parser import tokenize

ROOT = Path(__file__).resolve().parents[1]

def parse_ftb(text):
    # FTB permits newline separators where standard SNBT requires a comma.
    tokens = list(tokenize(text))
    ends = {'STRING', 'QUOTED_STRING', 'NUMBER', 'CLOSE_BRACKET', 'CLOSE_COMPOUND'}
    separators = {'COMMA', 'COLON', 'CLOSE_BRACKET', 'CLOSE_COMPOUND'}
    pieces = []
    for index, token in enumerate(tokens):
        pieces.append(token.value)
        if index + 1 < len(tokens) and token.type in ends and tokens[index+1].type not in separators:
            gap = text[token.span[0]+len(token.value):tokens[index+1].span[0]]
            assert '\n' in gap, 'Missing SNBT separator'
            pieces.append(',')
    return nbtlib.parse_nbt(''.join(pieces))

def validate():
    quests_dir = ROOT / 'overrides/config/ftbquests/quests'
    lang = parse_ftb((quests_dir / 'lang/en_us.snbt').read_text(encoding='utf-8'))
    quests, identifiers, chapters = {}, set(), []
    for path in sorted((quests_dir / 'chapters').glob('*.snbt')):
        chapter = parse_ftb(path.read_text(encoding='utf-8'))
        chapters.append(chapter)
        assert f"chapter.{chapter['id']}.title" in lang, path
        objects = [chapter]
        for quest in chapter['quests']:
            qid = str(quest['id'])
            assert f'quest.{qid}.title' in lang, qid
            assert f'quest.{qid}.quest_desc' in lang, qid
            assert quest.get('tasks'), qid
            quests[qid] = quest
            objects += [quest, *quest.get('tasks', []), *quest.get('rewards', [])]
        for obj in objects:
            ident = str(obj['id'])
            assert ident not in identifiers, f'Duplicate identifier: {ident}'
            identifiers.add(ident)
    visited, active = set(), set()
    def visit(qid):
        assert qid in quests, f'Missing prerequisite: {qid}'
        assert qid not in active, f'Cycle at {qid}'
        if qid in visited: return
        active.add(qid)
        for dependency in quests[qid].get('dependencies', []): visit(str(dependency))
        active.remove(qid); visited.add(qid)
    for qid in quests: visit(qid)
    for next_id, previous_id in [('1200000000000001','1100000000000005'),('1300000000000001','1200000000000003'),('1400000000000001','1300000000000004')]:
        assert previous_id in quests[next_id]['dependencies'], (next_id, previous_id)
    book = ROOT / 'overrides/patchouli_books/tumo_cs'
    categories = {p.stem for p in (book/'en_us/categories').glob('*.json')}
    entries = list((book/'en_us/entries').glob('*.json'))
    for path in book.rglob('*.json'):
        data = json.loads(path.read_text(encoding='utf-8'))
        if path.parent.name == 'entries':
            assert data['category'].split(':')[-1] in categories, path
            assert data.get('pages'), path
    lock = json.loads((ROOT/'pack.lock.json').read_text())
    names = set()
    for item in lock['mods']:
        assert Path(item['file']).name == item['file'] and item['file'].endswith('.jar')
        assert item['file'] not in names
        names.add(item['file'])
        assert item['url'].startswith('https://'), item['file']
        assert len(item['sha512']) == 128 and len(item['sha256']) == 64 and len(item['sha1']) == 40
        assert item['size'] > 0
    for path in (ROOT/'overrides').rglob('*.toml'):
        tomllib.loads(path.read_text(encoding='utf-8'))
    world = ROOT/'world-template/Blocklabor'
    assert 'Player' not in nbtlib.load(world/'level.dat')['Data']
    forbidden = {'playerdata','advancements','stats','ftbquests','ftbteams','ftbchunks','logs','servers.dat','usercache.json','session.lock'}
    for p in world.rglob('*'): assert p.name not in forbidden, p
    assert len(chapters) == 4 and len(quests) == 18 and len(entries) == 21
    result={'chapters':len(chapters),'quests':len(quests),'book_entries':len(entries),'locked_mods':len(names),'unique_quest_objects':len(identifiers)}
    print(json.dumps(result,indent=2))
    return result

if __name__ == '__main__': validate()
