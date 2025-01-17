import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image
import os
import sys
import traceback

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("zpy_trans_Pic")
        self.root.geometry("600x400")
        
        # 添加以下配置
        self.root.resizable(True, True)  # 允许调整窗口大小
        self.root.minsize(600, 400)      # 设置最小窗口大小
        
        # 配置网格权重，使界面更具响应性
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Variables to store paths and format
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.selected_format = tk.StringVar()
        
        # Supported formats
        self.formats = [
            'PNG', 'JPEG', 'BMP', 'GIF', 'TIFF', 'ICO', 'WEBP'
        ]
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Input Image", padding="5")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        input_frame.grid_columnconfigure(0, weight=1)
        
        input_entry = ttk.Entry(input_frame, textvariable=self.input_path)
        input_entry.grid(row=0, column=0, padx=5, sticky=(tk.W, tk.E))
        ttk.Button(input_frame, text="Browse", command=self.select_input).grid(row=0, column=1, padx=5)
        
        # Format selection
        format_frame = ttk.LabelFrame(main_frame, text="Output Format", padding="5")
        format_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        format_frame.grid_columnconfigure(0, weight=1)
        
        format_combo = ttk.Combobox(format_frame, textvariable=self.selected_format, values=self.formats)
        format_combo.grid(row=0, column=0, padx=5, sticky=(tk.W, tk.E))
        format_combo.set(self.formats[0])
        # Add callback for format change
        format_combo.bind('<<ComboboxSelected>>', self.on_format_change)
        
        # Output section
        output_frame = ttk.LabelFrame(main_frame, text="Output Location", padding="5")
        output_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        output_frame.grid_columnconfigure(0, weight=1)
        
        output_entry = ttk.Entry(output_frame, textvariable=self.output_path)
        output_entry.grid(row=0, column=0, padx=5, sticky=(tk.W, tk.E))
        ttk.Button(output_frame, text="Browse", command=self.select_output).grid(row=0, column=1, padx=5)
        
        # Convert button
        convert_button = ttk.Button(main_frame, text="Convert", command=self.convert_image)
        convert_button.grid(row=3, column=0, columnspan=2, pady=20)
        
    def select_input(self):
        filetypes = (
            ('All Images', '*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff;*.ico;*.webp'),
            ('All files', '*.*')
        )
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.input_path.set(filename)
            # Auto-set output path with new extension
            input_dir = os.path.dirname(filename)
            input_name = os.path.splitext(os.path.basename(filename))[0]
            # 自动设置输出文件名，添加转换后的格式后缀
            self.output_path.set(os.path.join(input_dir, f"{input_name}_converted.{self.selected_format.get().lower()}"))
    
    def select_output(self):
        try:
            # Get the current format
            current_format = self.selected_format.get().lower()
            
            # Get initial directory and filename
            if self.input_path.get():
                initial_dir = os.path.dirname(self.input_path.get())
                input_name = os.path.splitext(os.path.basename(self.input_path.get()))[0]
                # 默认输出文件名添加"_converted"后缀
                initial_file = f"{input_name}_converted"
            else:
                initial_dir = os.path.expanduser("~")
                initial_file = "untitled"
            
            # Create suggested filename with selected format
            suggested_filename = f"{initial_file}.{current_format}"
            
            # Show the save dialog
            filename = filedialog.asksaveasfilename(
                initialdir=initial_dir,
                initialfile=suggested_filename,
                defaultextension=f".{current_format}",
                filetypes=[
                    (f"{current_format.upper()} files", f"*.{current_format}"),
                    ("All files", "*.*")
                ],
                confirmoverwrite=True
            )
            
            # Handle the selected filename
            if filename:
                # Convert to absolute path
                filename = os.path.abspath(filename)
                
                # Ensure correct extension
                if not filename.lower().endswith(f".{current_format}"):
                    filename = f"{filename}.{current_format}"
                
                # Update the output path
                self.output_path.set(filename)
                
                # Force update the UI
                self.root.update_idletasks()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error selecting output location: {str(e)}")
    
    def convert_image(self):
        if not self.input_path.get():
            messagebox.showerror("Error", "Please select an input image!")
            return
        if not self.output_path.get():
            messagebox.showerror("Error", "Please select an output location!")
            return
            
        try:
            # Open and convert image
            with Image.open(self.input_path.get()) as img:
                # Convert to RGB if saving as JPEG
                if self.selected_format.get() == 'JPEG':
                    img = img.convert('RGB')
                img.save(self.output_path.get(), format=self.selected_format.get())
            messagebox.showinfo("Success", "Image converted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def on_format_change(self, event=None):
        # Update output path with new format if input file is selected
        if self.input_path.get() and self.output_path.get():
            current_output = self.output_path.get()
            dir_path = os.path.dirname(current_output)
            base_name = os.path.splitext(os.path.basename(current_output))[0]
            new_format = self.selected_format.get().lower()
            self.output_path.set(os.path.join(dir_path, f"{base_name}.{new_format}"))

# Add error logging
def setup_error_logging():
    if getattr(sys, 'frozen', False):
        # If running as exe
        application_path = os.path.dirname(sys.executable)
        log_path = os.path.join(application_path, 'error_log.txt')
        sys.stderr = open(log_path, 'w')

def main():
    try:
        setup_error_logging()
        root = tk.Tk()
        app = ImageConverterApp(root)
        root.mainloop()
    except Exception as e:
        error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
        with open('error_log.txt', 'w') as f:
            f.write(error_msg)
        messagebox.showerror("Error", f"An error occurred: {str(e)}\nCheck error_log.txt for details.")

if __name__ == "__main__":
    main() 