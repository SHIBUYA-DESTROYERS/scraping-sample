import sys
import os
from glob import glob
from collections import Counter

import MeCab


def main():
    """
    コマンドライン引数で指定したディレクトリ内のファイルを読み込んで，頻出単語を表示する．
    """

    input_dir = sys.argv[1]

    tagger = MeCab.Tagger('')
    tagger.parse('')

    frequency = Counter()
    count_processed = 0

    for path in glob(os.path.join(input_dir, '*', 'wiki_*')):
        print('Processing {0} ...'.format(path), file=sys.stderr)

        with open(path) as file:
            for content in iter_docs(file):
                tokens = get_tokens(tagger, content)
                frequency.update(tokens)

                count_processed += 1
                if count_processed % 10000 == 0:
                    print('{0} documents were processed.'.format(count_processed))

    for token, count in frequency.most_common(30):
        print(token, count)


def iter_docs(file):
    """
    ファイルオブジェクトを読み込んで，記事の中身を順に返すジェネレータ関数．
    """

    for line in file:
        if line.startswith('<doc '):
            buffer = []
        elif line.startswith('</doc>'):
            content = ''.join(buffer)
            yield content
        else:
            buffer.append(line)


def get_tokens(tagger, content):
    """
    文書内に出現した名詞のリストを取得する関数．
    """

    tokens = []

    node = tagger.parseToNode(content)
    while node:
        category, sub_category = node.feature.split(',')[:2]
        if category == '名詞' and sub_category in ('固有名詞', '一般'):
            tokens.append(node.surface)
        node = node.next

    return tokens


if __name__ == '__main__':
    main()
