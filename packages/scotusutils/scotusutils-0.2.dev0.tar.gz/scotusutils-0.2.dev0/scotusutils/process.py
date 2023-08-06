"""Functionality for processing documents"""

from scotusutils import pdftools


class TranscriptsProcessor(object):
    """
    Fully process & extract content from an Oral Argument Transcript PDF

    Parameters
    ----------
    transcript : class?
        Input transcript to process

    """

    def __init__(self, pdf_processor=pdftools.TranscriptsProcessor):
        # FIXME: Some concept of the steps to perform?
        pass

    def _process_transcript_document(self, transcript):
        # FIXME: What should this look like?
        try:
            pdf_proc = self._pdf_processor(transcript)
        except SUPDFProcessingError as err:
            logger.warning(
                (f"Encountered error processing transcript {transcript.id}: ")(f"{err}")
            )
            proc_transcript = None
