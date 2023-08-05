#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import API
from .jvm import *
from .data import Sentence, Word
from .types import POS
from typing import List, Union, Tuple, Set


class SentenceSplitter(object):
    """
    문장분리기를 생성합니다.

    :param str api: 문장분리기 API 패키지.
    """

    def __init__(self, api: str):
        self.__api = API._query(api, __class__.__name__)()

    def sentences(self, *text) -> List[str]:
        """
        문단(들)을 문장으로 분리합니다.

        :param Union[str,List[str]] text: 분석할 문단(들). 각 인자는 텍스트와 string 리스트 혼용 가능. (가변인자)
        :rtype: List[str]
        :return: 분리한 문장들. (flattened list)
        """
        result = []
        for paragraph in text:
            if type(paragraph) is list:
                result += self.sentences(*paragraph)
            elif type(paragraph) is str:
                result += py_list(self.__api.invoke(string(paragraph)), lambda x: x)
            else:
                raise TypeError('%s type은 문단 분리를 수행할 수 없습니다.' % (type(paragraph)))

        return result

    def __call__(self, *args, **kwargs) -> List[str]:
        """
        문단을 문장으로 분리합니다.

        :param Union[str,List[str]] text: 분석할 문단(들). 각 인자는 텍스트와 string 리스트 혼용 가능. (가변인자)
        :rtype: List[str]
        :return: 분리한 문장들. (flattened list)
        """
        return self.sentences(*args)

    @staticmethod
    def sentencesTagged(*text: List[Word]) -> List[Sentence]:
        """
        KoalaNLP가 구현한 문장분리기를 사용하여, 문단을 문장으로 분리합니다.

        :param Union[List[Word],Sentence] text: 분석할 문단(들). 각 인자는 품사표기가 되어있는 Word의 list 또는 Sentence 혼용 가능. (가변인자)
        :rtype: List[Sentence]
        :return: 분리된 문장들. (flattened list)
        """
        result = []
        for paragraph in text:
            if type(paragraph) is Sentence:
                reference = paragraph.getReference()
            elif type(paragraph) is list and len(paragraph) > 0:
                reference = Sentence(paragraph).getReference()
            else:
                raise TypeError('%s type은 sentencesTagged를 실행할 수 없습니다.' % (type(paragraph)))

            result += py_list(koala_class_of('proc', 'SentenceSplitter').INSTANCE.invoke(reference),
                              item_converter=Sentence.fromJava)

        return result


class Tagger(object):
    """
    품사분석기를 초기화합니다.

    :param str api: 사용할 품사분석기의 유형.
    :param str apiKey: ETRI 분석기의 경우, ETRI에서 발급받은 API Key
    :param bool useLightTagger: 코모란(KMR) 분석기의 경우, 경량 분석기를 사용할 것인지의 여부. (기본값 False)
    """

    def __init__(self, api: str, apiKey: str = '', useLightTagger: bool = False):
        if api == API.ETRI:
            self.__api = API._query(api, __class__.__name__)(apiKey)
        elif api == API.KMR:
            self.__api = API._query(api, __class__.__name__)(useLightTagger)
        else:
            self.__api = API._query(api, __class__.__name__)()

    def tag(self, *text: str) -> List[Sentence]:
        """
        문단(들)을 품사분석합니다.

        :param Union[str,List[str]] text: 분석할 문단들. 텍스트와 string 리스트 혼용 가능. (가변인자)
        :rtype: List[Sentence]
        :return: 분석된 결과. (flattened list)
        """
        result = []
        for paragraph in text:
            if type(paragraph) is list:
                result += self.tag(*paragraph)
            elif type(paragraph) is str:
                result += py_list(self.__api.tag(string(paragraph)), item_converter=Sentence.fromJava)
            else:
                raise TypeError('%s type은 품사 분석을 수행할 수 없습니다.' % (type(paragraph)))

        return result

    def tagSentence(self, *text: str) -> List[Sentence]:
        """
        문장을 품사분석합니다. (인자 하나를 문장 하나로 간주합니다)

        :param Union[str] text: 분석할 문장들. (가변인자)
        :rtype: List[Sentence]
        :return: 분석된 결과.
        """
        result = []
        for sentence in text:
            if type(sentence) is str:
                result.append(Sentence.fromJava(self.__api.tagSentence(string(sentence))))
            else:
                raise TypeError('%s type은 품사 분석을 수행할 수 없습니다.' % (type(sentence)))

        return result

    def __call__(self, *args, **kwargs) -> List[Sentence]:
        """
        문단(들)을 품사분석합니다.

        :param Union[str,List[str]] text: 분석할 문단들. 텍스트와 string 리스트 혼용 가능. (가변인자)
        :rtype: List[Sentence]
        :return: 분석된 결과. (flattened list)
        """
        return self.tag(*args)


class __CanAnalyzeProperty(object):
    """
    특성 부착형 분석기를 초기화합니다.

    :param str api: 사용할 분석기의 유형.
    :param str apiKey: ETRI 분석기의 경우, ETRI에서 발급받은 API Key
    """

    def __init__(self, api: str, cls: str, apiKey: str = ''):
        if api == API.ETRI:
            self.__api = API._query(api, cls)(apiKey)
        else:
            self.__api = API._query(api, cls)()

    def analyze(self, *text) -> List[Sentence]:
        """
        문단(들)을 분석합니다.

        :param Union[str,Sentence,List[str],List[Sentence]] text: 분석할 문단(들).
                각 인자는 텍스트(str), 문장 객체(Sentence), 텍스트의 리스트, 문장 객체의 리스트 혼용 가능 (가변인자)
        :rtype: List[Sentence].
        :return: 분석된 결과들. (flattened list)
        """
        result = []
        for paragraph in text:
            if type(paragraph) is str:
                result += py_list(self.__api.analyze(string(paragraph)), item_converter=Sentence.fromJava)
            elif type(paragraph) is Sentence:
                ref = paragraph.getReference()
                result.append(Sentence.fromJava(self.__api.analyze(ref)))
            elif type(paragraph) is list:
                result += self.analyze(*paragraph)
            else:
                raise Exception("List인 경우 Sentence의 List만 분석 가능합니다.")

        return result

    def __call__(self, *args, **kwargs) -> List[Sentence]:
        """
        문단(들)을 분석합니다.

        :param Union[str,Sentence,List[str],List[Sentence]] text: 분석할 문단(들).
                각 인자는 텍스트(str), 문장 객체(Sentence), 텍스트의 리스트, 문장 객체의 리스트 혼용 가능 (가변인자)
        :rtype: List[Sentence].
        :return: 분석된 결과들. (flattened list)
        """
        return self.analyze(*args)


class Parser(__CanAnalyzeProperty):
    """
    구문구조/의존구조분석기를 초기화합니다.

    :param str api: 사용할 분석기의 유형.
    :param str apiKey: ETRI 분석기의 경우, ETRI에서 발급받은 API Key
    """

    def __init__(self, api: str, apiKey: str = ''):
        super().__init__(api, __class__.__name__, apiKey)


class EntityRecognizer(__CanAnalyzeProperty):
    """
    개체명 인식기를 초기화합니다.

    :param str api: 사용할 분석기의 유형.
    :param str apiKey: ETRI 분석기의 경우, ETRI에서 발급받은 API Key
    """

    def __init__(self, api: str, apiKey: str = ''):
        super().__init__(api, __class__.__name__, apiKey)


class RoleLabeler(__CanAnalyzeProperty):
    """
    의미역 분석기를 초기화합니다.

    :param str api: 사용할 분석기의 유형.
    :param str apiKey: ETRI 분석기의 경우, ETRI에서 발급받은 API Key
    """

    def __init__(self, api: str, apiKey: str = ''):
        super().__init__(api, __class__.__name__, apiKey)


class Dictionary(object):
    """
    사용자 정의 사전을 연결합니다.

    :param str api: 사용자 정의 사전을 연결할 API 패키지.
    """

    def __init__(self, api: API):
        self.__api = API._query(api, __class__.__name__).INSTANCE

    def addUserDictionary(self, *pairs: Tuple[str, POS]):
        """
        사용자 사전에, 표면형과 그 품사를 추가.

        :param Tuple[str,POS] pairs: (표면형, 품사)의 가변형 인자
        """
        surface_list = [string(t[0]) for t in pairs]
        tag_list = [t[1].reference for t in pairs]
        self.__api.addUserDictionary(java_list(surface_list), java_list(tag_list))

    def contains(self, word: str, *pos_tags: POS) -> bool:
        """
        사전에 등재되어 있는지 확인합니다.

        :param str word: 확인할 형태소
        :param POS pos_tags: 세종품사들(기본값: NNP 고유명사, NNG 일반명사)
        :rtype: bool
        :return: 사전에 포함된다면 True 아니면 False.
        """
        if len(pos_tags) > 0:
            tags = pos_tags
        else:
            tags = [POS.NNP, POS.NNG]

        if len(tags) == 1:
            tag = tags[0]
            return self.__api.contains(java_tuple(string(word), tag.reference))
        else:
            return self.__api.contains(string(word), java_set([tag.reference for tag in tags]))

    def __contains__(self, item: Tuple[str, POS]) -> bool:
        """
        사전에 등재되어 있는지 확인합니다.

        :param Tuple[str,POS] item: 확인할 대상 (형태소, 품사)
        :rtype: bool
        :return: 사전에 포함된다면 True 아니면 False.
        """
        return self.contains(item[0], item[1])

    def importFrom(self, other, fastAppend=False, filter=lambda t: t.isNoun()):
        """
        다른 사전을 참조하여, 선택된 사전에 없는 단어를 사용자사전으로 추가합니다.

        :param Dictionary other: 참조할 사전
        :param bool fastAppend: 선택된 사전에 존재하는지를 검사하지 않고 빠르게 추가하고자 할 때. (기본값 False)
        :param Union[Set[POS],POS->bool] filter: 가져올 품사나, 품사의 리스트, 또는 해당 품사인지 판단하는 함수.
        """
        if type(filter) is not set:
            filter = {tag.name for tag in POS.values() if filter(tag)}
        else:
            filter = {tag.name for tag in filter}

        self.__api.importFrom(other.__api, fastAppend, java_pos_filter(filter))

    def getBaseEntries(self, filter=lambda t: t.isNoun()):
        """
        원본 사전에 등재된 항목 중에서, 지정된 형태소의 항목만을 가져옵니다. (복합 품사 결합 형태는 제외)

        :param Union[Set[POS],POS->bool] filter: 가져올 품사나, 품사의 리스트, 또는 해당 품사인지 판단하는 함수.
        :rtype: generator
        :return: (형태소, 품사)의 generator
        """
        if type(filter) is not set:
            filter = [tag.name for tag in POS.values() if filter(tag)]
        else:
            filter = {tag.name for tag in filter}

        entries = self.__api.getBaseEntries(java_pos_filter(filter))
        while entries.hasNext():
            item = entries.next()
            yield (item.getFirst(), POS.valueOf(item.getSecond().name()))

    def getItems(self) -> List[Tuple[str, POS]]:
        """
        사용자 사전에 등재된 모든 항목을 가져옵니다.

        :rtype: List[(str,POS)]
        :return: (형태소, 품사)의 set
        """

        return py_list(self.__api.getItems(),
                       item_converter=lambda t: (t.getFirst(), POS.valueOf(t.getSecond().name())))

    def getNotExists(self, onlySystemDic: bool, *word: Tuple[str, POS]) -> List[Tuple[str, POS]]:
        """
        사전에 등재되어 있는지 확인하고, 사전에 없는단어만 반환합니다.

        :param bool onlySystemDic: 시스템 사전에서만 검색할지 결정합니다.
        :param Tuple[str,POS] word: 확인할 (형태소, 품사)들의 가변인자
        :rtype: List[(str,POS)]
        :return: 사전에 없는 단어들.
        """

        zipped = [java_tuple(string(t[0]), t[1].reference) for t in word]

        return py_list(self.__api.getNotExists(onlySystemDic, java_varargs(zipped, class_of('kotlin.Pair'))),
                       item_converter=lambda t: (t.getFirst(), POS.valueOf(t.getSecond().name())))


# ----- Define members exported -----

__all__ = ['SentenceSplitter', 'Tagger', 'Parser', 'EntityRecognizer', 'RoleLabeler', 'Dictionary']
