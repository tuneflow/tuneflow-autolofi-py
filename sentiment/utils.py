from sentiment.data import PRESET_PARAGRAPH_SENTIMENTS, NUM_PARAGRAPHS_THRESHOLDS_OF_CLIMAX_LEVELS
from sentiment.consts import Sentiment
import random
import math
from typing import List


class SentimentUtils:
    @staticmethod
    def getParagraphSentiments(numParagraphs: int):
        '''
        Segment music of given length and label each segment with sentiment
        * Requirements:
        *    a. Music starts and ends up with S
        *    b. Climax shows up at the second half
        *    c. No abrupt sentiment increase
        '''
        # Use paragraph sentiment presets for short pieces
        if (numParagraphs in PRESET_PARAGRAPH_SENTIMENTS):
            return PRESET_PARAGRAPH_SENTIMENTS[numParagraphs][
                random.randint(0, len(PRESET_PARAGRAPH_SENTIMENTS[numParagraphs]) - 1)
            ]

        # Randomly generate paragraph sentiments for longer pieces.
        paragraphSentiments = [Sentiment.S] * numParagraphs

        if (numParagraphs not in PRESET_PARAGRAPH_SENTIMENTS):
            # TODO
            return paragraphSentiments

        # Step 1: Pick up the climax within the second half music
        climaxIndex = random.randint(math.ceil(numParagraphs / 2 + 0.5), numParagraphs - 2)
        maxSentiment = Sentiment.D if numParagraphs > NUM_PARAGRAPHS_THRESHOLDS_OF_CLIMAX_LEVELS[
            Sentiment.D] else Sentiment.C
        paragraphSentiments[climaxIndex] = maxSentiment

        return paragraphSentiments

    @staticmethod
    def getBarSentiments(numBars: int, numParagraphs: int):
        paragraphSentiments = SentimentUtils.getParagraphSentiments(numParagraphs)
        print(paragraphSentiments)
        barSentiments: List[Sentiment] = []
        for paragraph in paragraphSentiments:
            barSentiments.extend([paragraph] * 4)
        return barSentiments[0: numBars]
