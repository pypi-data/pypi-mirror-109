'''
@Author: meowmeowmeowcat
@Project Name: Toolbox-cli
'''

import sys
import click
import platform
from colorama import init,Fore, Back, Style
import os
import socket
import webbrowser
from pathlib import Path

# initialise Colorama
init()

@click.group()
@click.version_option("0.0.7")
def cli():
    """A Toolbox runs in Command Line"""
    pass

# Get System Info
@cli.command()
def system_info():
    """Get System Information"""
    uname = platform.uname()
    click.echo(Fore.BLUE + "=========System Information=========")
    click.echo(Style.RESET_ALL)
    click.echo(f"System: {uname.system}")
    click.echo(f"Node Name: {uname.node}")
    click.echo(f"Release: {uname.release}")
    click.echo(f"Version: {uname.version}")
    click.echo(f"Machine: {uname.machine}")
    click.echo(f"Processor: {uname.processor}")

@cli.command()
def qrcode():
    """Generate QR code"""
    click.echo(Fore.BLUE + "=========Generate QR code=========\n")
    click.echo(Style.RESET_ALL)
    try:
        import qrcode
    except ImportError:
        click.echo("Downloading 'qrcode' from https://pypi.org/project/qrcode ...")
        os.system("pip install qrcode")
        click.echo(Fore.YELLOW  + "RELOAD THE TOOLBOX! ")
        click.echo(Style.RESET_ALL)
        exit()
    text_input_qr_code = input("Please enter some text here: ")
    img = qrcode.make(text_input_qr_code)
    img.show()

@cli.command()
def get_ip():
    """Get Your IP Address"""
    click.echo(Fore.BLUE + "=========Get Your IP Address=========")
    click.echo(Style.RESET_ALL)
    click.echo(Fore.YELLOW + "Your IP Address is: " + socket.gethostbyname(socket.gethostname()))
    click.echo(Style.RESET_ALL)

@cli.command()
def speedtest():
    """Run Speedtest"""
    try:
        import speedtest
    except ImportError:
        click.echo("Downloading 'speedtest-cli' from https://pypi.org/project/speedtest-cli  ...")
        os.system("pip install speedtest-cli")
        click.echo(Fore.YELLOW  + "RELOAD THE TOOLBOX! ")
        click.echo(Style.RESET_ALL)
        exit()
        
    st = speedtest.Speedtest()
    click.echo("=========Run Speedtest=========")
    option = int(input('''What speed do you want to test:  
  
                              1) Download Speed  
  
                              2) Upload Speed  
  
                              3) Ping 
  
                              Your Choice: '''))
    
    download = st.download()
    upload = st.upload()
    
    # convert to Mbps
    download = download/1000000
    upload = upload/1000000
    
    if option == 1:  
        click.echo('Testing... Please wait')
        print(Fore.BLUE + "Your Download speed is", round(download, 5), 'Mbps')
        click.echo(Style.RESET_ALL)
  
    elif option == 2: 
        click.echo('Testing... Please wait')
        print(Fore.BLUE + "Your Upload speed is", round(upload, 5), 'Mbps') 
        click.echo(Style.RESET_ALL)
            
    elif option == 3:  
        click.echo('Testing... Please wait')
        st.get_servers([])
        ping = st.results.ping 
        print(Fore.BLUE + "Your Ping is ", ping )  
        click.echo(Style.RESET_ALL)
  
    else:
        click.echo(Fore.RED + "Please enter the correct choice !")
        click.echo(Style.RESET_ALL) 

# centimeter to meter
@cli.command()
@click.argument('m1', type=float, required=True)
def m_to_cm(m1):
    """Centimeter to Meter Converter"""
    cm1 = m1 * 100
    click.echo(Fore.YELLOW + f'Result: {cm1} cm')
    click.echo(Style.RESET_ALL)

# meter to centimeter
@cli.command()
@click.argument('cm2', type=float, required=True)
def cm_to_m(cm2):
    """Meter to Centimeter Converter"""
    m2 = cm2 / 100
    click.echo(Fore.YELLOW + f"Result: {m2} m")
    click.echo(Style.RESET_ALL)

# °C to °F (Celsius to Fahrenheit)
@cli.command()
@click.argument('c1', type=float, required=True)
def c_to_f(c1):
    """°C to °F (Celsius to Fahrenheit) Converter"""
    f1 = 9 / 5 * c1 + 32
    new_f1 = round(f1, 5)
    click.echo(Fore.YELLOW + "Result: {:.2f} °F".format(new_f1))
    click.echo(Style.RESET_ALL)

# °F to °C (Fahrenheit to Celsius)
@cli.command()
@click.argument('f2', type=float, required=True)
def f_to_c(f2):
    """°F to °C (Fahrenheit to Celsius) Converter"""
    c2 = (f2 - 32) * 5/9
    new_c2 = round(c2, 5)
    click.echo(Fore.YELLOW + "Result: {:.2f} °C".format(new_c2))
    click.echo(Style.RESET_ALL)

# Decimal to Hexadecimal
@cli.command()
@click.argument('d1', type=float, required=True)
def d_to_h(d1):
    """Decimal to Hexadecimal Converter"""
    h1 = float.hex(d1)[2:]
    click.echo(Fore.YELLOW + 'Result: ' + h1)
    click.echo(Style.RESET_ALL)

@cli.command()
def str_to_morse():
    """Encrypt the string to morse code"""
    click.echo(Fore.BLUE + "=========Encrypt the string to morse code=========")
    try:
        import morse_talk as mtalk
    except ImportError:
        click.echo("Downloading 'morse-talk' from https://pypi.org/project/morse-talk ...")
        os.system("pip install qrcode")
        click.echo(Fore.YELLOW  + "RELOAD THE TOOLBOX! ")
        click.echo(Style.RESET_ALL)
        exit()
    encrypt_message = input("Please enter the text you want to encrypt: ")
    encrypt_result = mtalk.encode(encrypt_message)
    click.echo(Fore.YELLOW + "Result: " + encrypt_result)
    click.echo(Style.RESET_ALL)
    
@cli.command()
def morse_to_str():
    """Decrypt morse code to string"""
    click.echo(Fore.BLUE + "=========Decrypt morse code to string=========")
    try:
        import morse_talk as mtalk
    except ImportError:
        click.echo("Downloading 'morse-talk' from https://pypi.org/project/morse-talk ...")
        os.system("pip install qrcode")
        click.echo(Fore.YELLOW  + "RELOAD THE TOOLBOX! ")
        click.echo(Style.RESET_ALL)
        exit()
    decrypt_message = input("Please enter the morse code you want to decrypt: ")
    decrypt_result = mtalk.decode(decrypt_message)
    click.echo(Fore.YELLOW + "Result: " + decrypt_result)
    click.echo(Style.RESET_ALL)
    
@cli.command()
def get_unicode():
    """Get Unicode code of a character"""
    click.echo(Fore.BLUE + "=========Get Unicode code of a character=========")
    character = input("Please enter the character that you want to get the Unicode of it (ONE CHARACTER ONLY): ")
    click.echo(ord(u"%s"%character))

@cli.command()
def issue():
    """Submit issue on Github"""
    webbrowser.open("https://github.com/meowmeowmeowcat/Toolbox-cli/issues")

@cli.command()
@click.argument('search_keywords_google', type=str, required=True)
def google(search_keywords_google):
    """Search Google"""
    webbrowser.open("https://www.google.com/search?q=" + search_keywords_google)

@cli.command()
@click.argument('search_keywords_duckduckgo', type=str, required=True)
def duckduckgo(search_keywords_duckduckgo):
    """Search Duckduckgo"""
    webbrowser.open("https://duckduckgo.com/?q=" + search_keywords_duckduckgo)

@cli.command()
@click.argument('search_keywords_youtube', type=str, required=True)
def youtube(search_keywords_youtube):
    """Search Videos on Youtube"""
    webbrowser.open("https://www.youtube.com/results?search_query=" + search_keywords_youtube)

@cli.command()
def hand_drawn_style():
    """Convert Photo to Hand-Drawn Style"""
    try:
        import numpy as np
        from PIL import Image
    except ImportError:
        click.echo("""
                   Downloading 'numpy' from https://pypi.org/project/numpy ...
                   Downloading 'Pillow' from https://pypi.org/project/Pillow/ ...
                   """)
        os.system("pip install numpy")
        os.system("pip install Pillow")
        click.echo(Fore.YELLOW  + "RELOAD THE TOOLBOX! ")
        click.echo(Style.RESET_ALL)
        exit()
    
    click.echo(Fore.BLUE + "=========Convert Photo to Hand-Drawn Style=========")
    click.echo(Style.RESET_ALL)
    
    path = input(r"Please enter path of the photo: ")
    
    if os.path.isfile(path):
        a = np.asarray(Image.open(path).convert("L")).astype('float')

        depth = 10.  
        grad = np.gradient(a)  
        grad_x, grad_y = grad  
        grad_x = grad_x * depth / 100.
        grad_y = grad_y * depth / 100.
        A = np.sqrt(grad_x ** 2 + grad_y ** 2 + 1.)
        uni_x = grad_x / A
        uni_y = grad_y / A
        uni_z = 1. / A

        vec_el = np.pi / 2.2  
        vec_az = np.pi / 4.  
        dx = np.cos(vec_el) * np.cos(vec_az)  
        dy = np.cos(vec_el) * np.sin(vec_az)  
        dz = np.sin(vec_el)  

        b = 255 * (dx * uni_x + dy * uni_y + dz * uni_z)  
        b = b.clip(0, 255)

        im = Image.fromarray(b.astype('uint8'))  
        im.save(path + "output.jpg")

        click.echo(Fore.YELLOW + "Finished! Saved as 'output.jpg'")
    else:
        click.echo(Fore.BLUE + "Please enter a valid image path! ")
    
@cli.command()
def list():
    """Tools you can use in this toolbox"""
    click.echo(Fore.YELLOW + """
                *: Need to install other packages
                
                Get Unicode Of A Character         Usage: get-unicode
                Get System Info                    Usage: system-info 
                Get IP Address                     Usage: get-ip
                *Run Speedtest                     Usage: speedtest
                *Generate QR code                  Usage: qrcode
                *Encrypt text to morse code        Usage: str-to-morse
                *Decrypt morse code to text        Usage: morse-to-str
                Submit issue on Github             Usage: issue
                Search on Google                   Usage: google
                Search on DuckDuckGo               Usage: duckduckgo
                Search on YouTube                  Usage: youtube
                Convert Photo to Hand-Drawn Style  Usage: hand-drawn-style
                
                Unit Converter:
                °F to °C (Fahrenheit to Celsius) Usage: f-to-c  [number(Fahrenheit)]
                °C to °F (Celsius to Fahrenheit) Usage: c-to-f  [number(Celsius)]
                Centimeter to Meter              Usage: cm-to-m [number(Centimeter)]
                Meter to Centimeter              Usage: m-to-cm [number(Meter)]
                Decimal to Hexadecimal           Usage: d-to-h  [number(Decimal)]
                """)

if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("Toolbox")
    cli()
