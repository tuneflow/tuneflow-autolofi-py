from sentiment.consts import Sentiment
from typing import List, Dict

PRESET_PARAGRAPH_SENTIMENTS: Dict[int, List[List[Sentiment]]] = {
    2: [
        [Sentiment.S, Sentiment.A],
        [Sentiment.A, Sentiment.B],
        [Sentiment.A, Sentiment.A],
        [Sentiment.B, Sentiment.S],
    ],
    3: [
        [Sentiment.A, Sentiment.B, Sentiment.A],
        [Sentiment.A, Sentiment.B, Sentiment.C],
        [Sentiment.A, Sentiment.B, Sentiment.S],
        [Sentiment.B, Sentiment.A, Sentiment.C],
    ],
    4: [
        [Sentiment.S, Sentiment.A, Sentiment.B, Sentiment.S],
        [Sentiment.S, Sentiment.A, Sentiment.A, Sentiment.S],
        [Sentiment.S, Sentiment.A, Sentiment.B, Sentiment.C],
    ],
    5: [
        [Sentiment.S, Sentiment.A, Sentiment.B, Sentiment.C, Sentiment.S],
        [Sentiment.S, Sentiment.A, Sentiment.A, Sentiment.B, Sentiment.S],
        [Sentiment.S, Sentiment.A, Sentiment.S, Sentiment.B, Sentiment.S],
        [Sentiment.S, Sentiment.A, Sentiment.B, Sentiment.C, Sentiment.D],
    ],
    6: [
        [Sentiment.S, Sentiment.S, Sentiment.A, Sentiment.B, Sentiment.S, Sentiment.S],
        [Sentiment.S, Sentiment.A, Sentiment.A, Sentiment.B, Sentiment.B, Sentiment.S],
        [Sentiment.S, Sentiment.A, Sentiment.B, Sentiment.C, Sentiment.D, Sentiment.S],
        [Sentiment.S, Sentiment.S, Sentiment.A, Sentiment.B, Sentiment.C, Sentiment.S],
    ],
    7: [
        [Sentiment.S, Sentiment.A, Sentiment.A, Sentiment.S, Sentiment.B, Sentiment.B, Sentiment.S],
        [Sentiment.S, Sentiment.A, Sentiment.S, Sentiment.B, Sentiment.S, Sentiment.C, Sentiment.S],
        [Sentiment.S, Sentiment.A, Sentiment.A, Sentiment.B, Sentiment.B, Sentiment.C, Sentiment.S],
        [Sentiment.S, Sentiment.S, Sentiment.A, Sentiment.A, Sentiment.B, Sentiment.B, Sentiment.C],
    ],
}

PRESET_PARAGRAPH_SENTIMENTS_: Dict[int, List[List[Sentiment]]] = {
    2: [
        [Sentiment.A, Sentiment.B],
        [Sentiment.A, Sentiment.A],
        [Sentiment.B, Sentiment.A],
    ],
    3: [
        [Sentiment.A, Sentiment.B, Sentiment.A],
        [Sentiment.A, Sentiment.B, Sentiment.C],
        [Sentiment.A, Sentiment.B, Sentiment.B],
        [Sentiment.B, Sentiment.A, Sentiment.C],
    ],
    4: [
        [Sentiment.S, Sentiment.A, Sentiment.B, Sentiment.B],
        [Sentiment.S, Sentiment.A, Sentiment.A, Sentiment.B],
        [Sentiment.S, Sentiment.A, Sentiment.B, Sentiment.C],
    ],
    5: [
        [Sentiment.S, Sentiment.A, Sentiment.B, Sentiment.C, Sentiment.B],
        [Sentiment.S, Sentiment.A, Sentiment.A, Sentiment.B, Sentiment.A],
        [Sentiment.S, Sentiment.A, Sentiment.A, Sentiment.B, Sentiment.B],
        [Sentiment.S, Sentiment.A, Sentiment.B, Sentiment.C, Sentiment.D],
    ],
    6: [
        [Sentiment.S, Sentiment.A, Sentiment.A, Sentiment.B, Sentiment.B, Sentiment.A],
        [Sentiment.S, Sentiment.A, Sentiment.A, Sentiment.B, Sentiment.C, Sentiment.B],
        [Sentiment.S, Sentiment.A, Sentiment.B, Sentiment.C, Sentiment.D, Sentiment.C],
        [Sentiment.S, Sentiment.A, Sentiment.B, Sentiment.B, Sentiment.C, Sentiment.C],
    ],
    7: [
        [Sentiment.S, Sentiment.A, Sentiment.A, Sentiment.B, Sentiment.B, Sentiment.C, Sentiment.C],
        [Sentiment.S, Sentiment.A, Sentiment.A, Sentiment.B, Sentiment.C, Sentiment.C, Sentiment.D],
        [Sentiment.S, Sentiment.A, Sentiment.B, Sentiment.C, Sentiment.D, Sentiment.C, Sentiment.B],
        [Sentiment.S, Sentiment.A, Sentiment.B, Sentiment.C, Sentiment.C, Sentiment.B, Sentiment.A],
    ],
    8: [
        [
            Sentiment.S,
            Sentiment.A,
            Sentiment.A,
            Sentiment.B,
            Sentiment.B,
            Sentiment.C,
            Sentiment.C,
            Sentiment.D,
        ],
        [
            Sentiment.S,
            Sentiment.A,
            Sentiment.A,
            Sentiment.A,
            Sentiment.B,
            Sentiment.B,
            Sentiment.A,
            Sentiment.A,
        ],
        [
            Sentiment.S,
            Sentiment.A,
            Sentiment.B,
            Sentiment.B,
            Sentiment.C,
            Sentiment.C,
            Sentiment.D,
            Sentiment.D,
        ],
        [
            Sentiment.S,
            Sentiment.A,
            Sentiment.B,
            Sentiment.B,
            Sentiment.A,
            Sentiment.B,
            Sentiment.C,
            Sentiment.C,
        ],
    ],
}

NUM_PARAGRAPHS_THRESHOLDS_OF_CLIMAX_LEVELS = {
}

NUM_PARAGRAPHS_THRESHOLDS_OF_CLIMAX_LEVELS[Sentiment.S] = 2
NUM_PARAGRAPHS_THRESHOLDS_OF_CLIMAX_LEVELS[Sentiment.A] = 2
NUM_PARAGRAPHS_THRESHOLDS_OF_CLIMAX_LEVELS[Sentiment.B] = 2
NUM_PARAGRAPHS_THRESHOLDS_OF_CLIMAX_LEVELS[Sentiment.C] = 3
NUM_PARAGRAPHS_THRESHOLDS_OF_CLIMAX_LEVELS[Sentiment.D] = 11
