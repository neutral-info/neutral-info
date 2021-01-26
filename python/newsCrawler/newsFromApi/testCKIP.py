from ckiptagger import WS, POS, NER


def simple_demo():
    text = "傅達仁今將執行安樂死，卻突然爆出自己20年前遭緯來體育台封殺，他不懂自己哪裡得罪到電視台。"

    ws_results = ws([text])
    pos_results = pos(ws_results)
    ner_results = ner(ws_results, pos_results)

    # print(ner_results)
    # print(pos_results)
    for name in ner_results[0]:
        print(name[3])


def print_word_pos_sentence(word_sentence, pos_sentence):
    assert len(word_sentence) == len(pos_sentence)
    for word, pos in zip(word_sentence, pos_sentence):
        print(f"22{word}({pos})", end="\u3000")
    print()
    return


def main():
    sentence_list = [
        "傅達仁今將執行安樂死，卻突然爆出自己20年前遭緯來體育台封殺，他不懂自己哪裡得罪到電視台。",
        "美國參議院針對今天總統布什所提名的勞工部長趙小蘭展開認可聽證會，預料她將會很順利通過參議院支持，成為該國有史以來第一位的華裔女性內閣成員。",
        "",
        "土地公有政策?？還是土地婆有政策。.",
        "… 你確定嗎… 不要再騙了……",
        "最多容納59,000個人,或5.9萬人,再多就不行了.這是環評的結論.",
        "科長說:1,坪數對人數為1:3。2,可以再增加。",
    ]

    ws = WS("./data")
    pos = POS("./data")
    ner = NER("./data")

    word_sentence_list = ws(
        sentence_list,
        # sentence_segmentation = True, # To consider delimiters
        # segment_delimiter_set = {",", "。", ":", "?", "!", ";"}), # This is the defualt set of delimiters
        # recommend_dictionary = dictionary1, # words in this dictionary are encouraged
        # coerce_dictionary = dictionary2, # words in this dictionary are forced
    )

    pos_sentence_list = pos(word_sentence_list)

    entity_sentence_list = ner(word_sentence_list, pos_sentence_list)

    for i, sentence in enumerate(sentence_list):
        print()
        print(f"'11{sentence}'")
        print_word_pos_sentence(word_sentence_list[i], pos_sentence_list[i])
        for entity in sorted(entity_sentence_list[i]):
            print(f"33-{entity[2]},{entity[3]}")


if __name__ == "__main__":
    main()