from PIL import Image, ImageDraw, ImageFont
def GenerateImg(score):
    

    img = Image.new('RGB', (500, 500), color = "white")
    
    fnt = ImageFont.truetype('C:\Windows\Fonts\consola.ttf', 225)
    d = ImageDraw.Draw(img)
    w,h = d.textsize(score, font=fnt)
    d.text(((500-w)/2, (500-h)/2), score, font=fnt, fill="black")
    
    img.save('pil_text_font.png')

GenerateImg("125")