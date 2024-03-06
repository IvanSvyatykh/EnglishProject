import cv2

from model.extractor import OcrToTableTool as ottt, TableExtractor as te, TableLinesRemover as tlr


class Convertor():
    def __init__(self, path: str):
        self.path = path

    def to_csv(self) -> None:
        path_to_image = self.path
        table_extractor = te.TableExtractor(path_to_image)
        perspective_corrected_image = table_extractor.execute()
        cv2.imshow("perspective_corrected_image", perspective_corrected_image)

        lines_remover = tlr.TableLinesRemover(perspective_corrected_image)
        image_without_lines = lines_remover.execute()
        cv2.imshow("image_without_lines", image_without_lines)

        ocr_tool = ottt.OcrToTableTool(image_without_lines, perspective_corrected_image,
                                       self.path.replace('.jpg', '.csv'))
        ocr_tool.execute()

        cv2.waitKey(0)
        cv2.destroyAllWindows()
