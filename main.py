import os
import tempfile
from cairosvg import svg2png
from pdf2image import convert_from_path
from pptx import Presentation
from pptx.util import Inches
import sys

def pdf_to_pptx(pdf_path, output_pptx):
    # PDF → PNG（各ページ）
    pages = convert_from_path(pdf_path)
    prs = Presentation()

    for i, page in enumerate(pages):
        # 一時ファイルに保存
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img:
            page.save(tmp_img.name, "PNG")
            slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank slide

            # スライドサイズに合わせて画像を挿入
            prs_width = prs.slide_width
            prs_height = prs.slide_height

            slide.shapes.add_picture(tmp_img.name, 0, 0, width=prs_width, height=prs_height)

            # 削除のためにパス保存
            img_path = tmp_img.name

        # 一時ファイル削除
        os.remove(img_path)

    prs.save(output_pptx)
    print(f"PowerPoint saved to {output_pptx}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_pdf> <output_pptx>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_pptx = sys.argv[2]

    if not os.path.exists(input_pdf):
        print(f"Error: {input_pdf} does not exist.")
        sys.exit(1)

    pdf_to_pptx(input_pdf, output_pptx)


