# Copyright 2019 Geneea Analytics s.r.o.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Reads the G3 object from a json-based dictionary as returned from Geneea G3 API.
#
# Except the fromDict, all functions and classes defined in this file are only internal helpers.
#
# Conventions:
# - variables prefixed with 'raw' refer to dictionaries based on the json objects returned by the API

import re
import warnings
from typing import List, Dict, Mapping, Any, Iterable, Optional, Tuple

from geneeanlpclient.common import ud
from geneeanlpclient.common.dictutil import JsonType, getValue
from geneeanlpclient.g3.model import (G3, CharSpan, Language, Sentiment, Paragraph, Sentence, Relation, Entity, Tag,
    TectoToken, Token, TreeBuilder, Tree, TokenSupport, Vector)

G3_KEYS = frozenset([
    'id', 'language', 'paragraphs',
    'entities', 'tags', 'relations',
    'docSentiment', 'itemSentiments', 'docVectors', 'itemVectors',
    'usedChars', 'metadata', 'debugInfo', 'version'
])
""" Standard keys used in G3 analysis json """


def fromDict(rawAnalysis: JsonType) -> G3:
    """
    Reads the G3 object from a json-based dictionary as returned from Geneea G3 API.
    """
    return _Reader()._fromDict(rawAnalysis)


class _Reader:

    def __init__(self) -> None:
        self.registry: Dict[str, Any] = {}

    def _register(self, obj: Any) -> None:
        self.registry[obj.id] = obj

    def _registerAll(self, objs: Optional[Iterable[Any]]) -> None:
        if objs:
            for obj in objs:
                self._register(obj)

    def resolveId(self, id: str) -> Optional[Any]:
        if id is None:
            return None
        try:
            return self.registry[id]
        except KeyError:
            raise KeyError(f'Unknown object id used as a reference: {id}')

    def resolveIds(self, ids: Iterable[str]) -> List[Any]:
        return list(filter(None, [self.resolveId(id) for id in ids]))

    @staticmethod
    def _checkVersion(rawAnalysis: JsonType) -> Tuple[int, int, int]:
        version = rawAnalysis.get('version', '3.0.0')
        verMatch = re.fullmatch(r'^([0-9]+)\.([0-9]+)\.([0-9]+)$', version)
        if not verMatch:
            raise ValueError(f'unsupported API version "{version}"')
        verMajor, verMinor, verFix = tuple(map(int, verMatch.groups()))
        if verMajor != 3 or verMinor > 1:
            raise ValueError(f'unsupported API version "{version}", major ver.num != 3 or minor ver.num > 1')
        return verMajor, verMinor, verFix

    @staticmethod
    def _readSentiment(rawSentiment: JsonType) -> Sentiment:
        return Sentiment(
            mean=rawSentiment['mean'],
            label=rawSentiment['label'],
            positive=rawSentiment['positive'],
            negative=rawSentiment['negative']
        )

    @staticmethod
    def _readItemSentiments(rawSentiments: JsonType) -> Mapping[str, Sentiment]:
        return {k:  _Reader._readSentiment(v) for k, v in rawSentiments.items()}

    @staticmethod
    def _readVectors(rawVectors: List[JsonType]) -> List[Vector]:
        return [Vector(
            name=vec['mean'],
            version=vec['version'],
            values=vec['values']
        ) for vec in rawVectors]

    @staticmethod
    def _readItemVectors(rawVectors: JsonType) -> Mapping[str, List[Vector]]:
        return {k: _Reader._readVectors(v) for k, v in rawVectors.items()}

    @staticmethod
    def _readToken(rawToken: Dict, tokenIdx: int) -> Token:
        """ transform raw token to token object """

        text = rawToken['text']
        corrText = rawToken['corrText']
        fncStr = rawToken.get('fnc')
        if fncStr:
            # legacy non-UD function 'clause'
            if fncStr.upper() == 'CLAUSE':
                fnc = ud.UDep.ROOT
            else:
                fnc = ud.UDep.fromStr(fncStr)
        else:
            fnc = None

        posStr = rawToken.get('pos')

        return Token(
            id=rawToken['id'],
            idx=tokenIdx,  # sentence based index
            text=text,
            charSpan=CharSpan.withLen(rawToken['off'], len(text)),
            corrText=corrText,
            corrCharSpan=CharSpan.withLen(rawToken['corrOff'], len(corrText)),
            deepLemma=rawToken.get('dLemma'),
            lemma=rawToken.get('lemma'),
            pos=ud.UPos.fromStr(posStr) if posStr else None,
            feats=rawToken.get('feats'),
            morphTag=rawToken.get('mTag'),
            fnc=fnc
        )

    @staticmethod
    def _readTokens(rawTokens: List[JsonType]) -> List[Token]:
        return [_Reader._readToken(rawToken, tokenIdx=idx) for idx, rawToken in enumerate(rawTokens)]

    def _createTree(self, rawTokens: List[JsonType], tokens: List[Token]) -> Tree[Token]:
        tb = TreeBuilder[Token]()
        tb.addNodes(tokens)

        for rawToken in rawTokens:
            if 'parId' in rawToken:
                parent = self.resolveId(rawToken['parId'])
                child = self.resolveId(rawToken['id'])
                tb.addDependency(childIdx=child.idx, parentIdx=parent.idx)

        return tb.build()

    def _readTectoToken(self, raw: JsonType, tokenIdx: int) -> TectoToken:
        tokens = self.resolveIds(raw.get('tokenIds', []))
        return TectoToken(
            id=raw['id'],
            idx=tokenIdx,  # sentence based index
            lemma=raw.get('lemma'),
            feats=raw.get('feats'),
            fnc=raw.get('fnc', ud.UDep.DEP.toStr()),
            tokenSupport=TokenSupport.of(tokens) if tokens else None,
            entityMention=raw.get('entityMentionId'),  # will be replaced by mention obj. later
            entity=None  # will be filled later
        )

    def _readTectoTokens(self, rawTokens: List[JsonType]) -> Tree[TectoToken]:
        tb = TreeBuilder[TectoToken]()

        for idx, rawToken in enumerate(rawTokens):
            tt = self._readTectoToken(rawToken, tokenIdx=idx)
            self._register(tt)
            tb.addNode(tt)

        for rawToken in rawTokens:
            if 'parId' in rawToken:
                parent = self.resolveId(rawToken['parId'])
                child = self.resolveId(rawToken['id'])
                tb.addDependency(childIdx=child.idx, parentIdx=parent.idx)

        return tb.build()

    def _readSentence(self, rawSentence: JsonType) -> Sentence:
        rawTokens = rawSentence.get('tokens', [])
        tokens = _Reader._readTokens(rawTokens)
        self._registerAll(tokens)

        if tokens[0].fnc:
            tree = self._createTree(rawTokens=rawTokens, tokens=tokens)
            tectoTree = self._readTectoTokens(rawSentence.get('tecto', []))
        else:
            tree = tectoTree = None

        sentence = Sentence(
            id=rawSentence['id'],
            root=tree.root if tree else None,
            tokens=tokens,
            tectoRoot=tectoTree.root if tectoTree else None,
            tectoTokens=tectoTree.tokens if tectoTree else [],
            sentiment=None  # will be filled later
        )
        self._register(sentence)

        for t in sentence.tokens:
            t.sentence = sentence

        for tt in sentence.tectoTokens:
            tt.sentence = sentence

        return sentence

    def _readParagraph(self, rawPara: JsonType) -> Paragraph:
        id = rawPara['id']
        sentences = [self._readSentence(rawS) for rawS in rawPara['sentences']]

        para = Paragraph(
            id=id,
            type=rawPara['type'],
            text=rawPara['text'],
            corrText=rawPara['corrText'],
            sentences=sentences
        )
        self._register(para)

        for s in para.sentences:
            s.paragraph = para

        return para

    def _readEntityMention(self, raw: JsonType) -> Entity.Mention:
        return Entity.Mention(
            id=raw['id'],
            mwl=raw['mwl'],
            text=raw['text'],
            tokenSupport=TokenSupport.of(self.resolveIds(raw.get('tokenIds', []))),
            derivedFrom=raw.get('derivedFromEntityId'),  # will be replaced by entity obj. later
            sentiment=None,  # will be filled later
            feats=raw.get('feats')
        )

    def _readEntity(self, raw: JsonType) -> Entity:
        rawMentions = raw.get('mentions', [])
        mentions = [self._readEntityMention(rm) for rm in rawMentions]
        self._registerAll(mentions)

        entity = Entity(
            id=raw['id'],
            gkbId=raw.get('gkbId'),
            stdForm=raw['stdForm'],
            entityType=raw['type'],
            feats=raw.get('feats'),
            mentions=mentions,
            sentiment=None  # will be filled later
        )

        for m in mentions:
            m.mentionOf = entity

        return entity

    def _readEntities(self, rawAnalysis: JsonType) -> List[Entity]:
        entities = [self._readEntity(raw) for raw in rawAnalysis.get('entities', [])]
        self._registerAll(entities)
        # fill derived-from entities for mentions
        for e in entities:
            for m in e.mentions:
                m.derivedFrom = self.resolveId(m.derivedFrom)
        return entities

    def _readTagMention(self, raw: JsonType) -> Tag.Mention:
        return Tag.Mention(
            id=raw['id'],
            tokenSupport=TokenSupport.of(self.resolveIds(raw.get('tokenIds', []))),
            sentiment=None,  # will be filled later
            feats=raw.get('feats')
        )

    def _readTag(self, raw: JsonType) -> Tag:
        mentions = [self._readTagMention(rm) for rm in raw.get('mentions', [])]
        self._registerAll(mentions)

        return Tag(
            id=raw['id'],
            gkbId=raw.get('gkbId'),
            stdForm=raw['stdForm'],
            tagType=raw['type'],
            relevance=raw['relevance'],
            feats=raw.get('feats'),
            mentions=mentions,
            sentiment=None  # will be filled later
        )

    def _readTags(self, rawAnalysis: JsonType) -> List[Tag]:
        tags = [self._readTag(raw) for raw in rawAnalysis.get('tags', [])]
        self._registerAll(tags)
        return tags

    def _readArg(self, raw: JsonType) -> Relation.Argument:
        return Relation.Argument(
            name=raw['name'],
            type=raw['type'],
            entity=self.resolveId(raw.get('entityId'))
        )

    def _readRelationSupport(self, raw: JsonType) -> Relation.Support:
        return Relation.Support(
            tokenSupport=TokenSupport.of(self.resolveIds(raw.get('tokenIds', []))),
            tectoToken=self.resolveId(raw.get('tectoId'))
        )

    def _readRelation(self, raw: JsonType) -> Relation:
        return Relation(
            id=raw['id'],
            name=raw['name'],
            textRepr=raw['textRepr'],
            type=raw['type'],
            args=[self._readArg(ra) for ra in raw.get('args', [])],
            feats=raw.get('feats'),
            support=[self._readRelationSupport(rs) for rs in raw.get('support', [])],
            sentiment=None  # will be filled later
        )

    def _readRelations(self, rawAnalysis: JsonType) -> List[Relation]:
        relations = [self._readRelation(raw) for raw in rawAnalysis.get('relations', [])]
        self._registerAll(relations)
        return relations

    def _fromDict(self, rawAnalysis: JsonType) -> G3:
        """
        :param rawAnalysis: dictionary corresponding to a G3 api json
        :return G3 object encapsulating the analysis

        Note: depending on requested set of analyses and language support many of the keys can be missing
        """
        versionMajor, versionMinor, versionFix = _Reader._checkVersion(rawAnalysis)
        useTopLevelMetadata = versionMinor < 2 and versionFix < 1

        metadata = rawAnalysis.get('metadata')

        unknownKeys = sorted(rawAnalysis.keys() - G3_KEYS)
        if unknownKeys:
            if useTopLevelMetadata and metadata is None:
                metadata = {key: rawAnalysis[key] for key in unknownKeys}
            else:
                warnings.warn(f'unrecognized fields in the analysis dict: {unknownKeys}')

        paragraphs = [self._readParagraph(raw) for raw in rawAnalysis.get('paragraphs', [])]
        entities = self._readEntities(rawAnalysis)
        tags = self._readTags(rawAnalysis)
        relations = self._readRelations(rawAnalysis)

        docSentiment = self._readSentiment(rawAnalysis['docSentiment']) if 'docSentiment' in rawAnalysis else None
        docVectors = self._readVectors(rawAnalysis['docVectors']) if 'docVectors' in rawAnalysis else None

        g3 = G3(
            docId=rawAnalysis.get('id'),
            language=Language(
                detected=getValue(rawAnalysis, 'language.detected', 'und')  # ISO 639-2 for Undetermined lg
            ),
            paragraphs=paragraphs,
            entities=entities,
            tags=tags,
            relations=relations,
            docSentiment=docSentiment,
            docVectors=docVectors,
            usedChars=rawAnalysis.get('usedChars'),
            metadata=metadata,
            debugInfo=rawAnalysis.get('debugInfo'),
        )

        for p in g3.paragraphs:
            p.container = g3

        # fill tecto token entity mention
        for tt in g3.tectoTokens:
            tt.entityMention = self.resolveId(tt.entityMention)
            tt.entity = tt.entityMention.mentionOf if tt.entityMention else None

        # fill items with their sentiment
        id2sentiment = self._readItemSentiments(rawAnalysis.get('itemSentiments', {}))
        for id, sentiment in id2sentiment.items():
            self.resolveId(id).sentiment = sentiment

        # fill items with their vectors
        id2vectors = self._readItemVectors(rawAnalysis.get('itemVectors', {}))
        for id, vectors in id2vectors.items():
            self.resolveId(id).vectors = vectors

        return g3
