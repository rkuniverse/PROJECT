import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw
import cv2

from sketchpy import canvas

parent = tk.Tk()
parent.title("Home")
parent.geometry("700x500")


def main():
    global iframe

    def askpath():
        entry = filedialog.askopenfilename(filetypes=[("JPG files", "*.jpg"), ("PNG files", "*.png")])
        return entry

    def process(path):

        def draw(path):
            sframe.destroy()
            image = Image.open(path)
            if path:

                obj = canvas.sketch_from_image(path)
                obj.draw(threshold=100)

                sketch_image = cv2.cvtColor(obj.image, cv2.COLOR_GRAY2BGR)

                output_path = filedialog.asksaveasfilename()
                cv2.imwrite(output_path, sketch_image)

                print('Sketch saved at:', output_path)
                print("good")
                pass
            else:
                print("error")
                return 0

            print(path)
            main()
            pass

        def enhance(path):
            import cv2
            import numpy as np

            def sharpen_image(image):

                kernel = np.array([[0, -1, 0],
                                   [-1, 5, -1],
                                   [0, -1, 0]])

                sharpened_image = cv2.filter2D(image, -1, kernel)
                return sharpened_image

            def denoise_image(image):

                denoised_image = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)
                return denoised_image

            image_path = path
            original_image = cv2.imread(image_path)

            if original_image is None:
                print('Error: Could not open or find the image.')
            else:

                sharpened_image = sharpen_image(original_image)

                denoised_sharpened_image = denoise_image(sharpened_image)

                cv2.imshow('Original Image', original_image)
                cv2.imshow('Sharpened Image', sharpened_image)
                cv2.imshow('Denoised Sharpened Image', denoised_sharpened_image)

                cv2.imwrite('sharpened_image.png', sharpened_image)
                cv2.imwrite('denoised_sharpened_image.png', denoised_sharpened_image)

                cv2.waitKey(0)
                cv2.destroyAllWindows()
            sframe.destroy()
            print(path)
            main()
            pass

        global iframe
        iframe.destroy()
        sframe = tk.Frame(parent)
        sframe.pack()
        b1 = tk.Button(sframe, text="DRAW", command=lambda: (draw(path)))

        b2 = tk.Button(sframe, text="ENHANCE", command=lambda: (enhance(path)))

        b1.pack()
        b2.pack()

    def function():
        path = askpath()

        if path:
            process(path)

        else:
            messagebox.showerror('', 'Canceled by user !')
            return 0

    iframe = tk.Frame(parent)
    iframe.pack()

    tk.Label(iframe, text="SELECT IMAGE PATH TO PROCESS", font=('', 18, 'bold')).pack()
    button = tk.Button(iframe, text="Select Image", command=function)
    button.pack()


main()
parent.mainloop()