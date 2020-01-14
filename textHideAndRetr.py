from PIL import Image
import textwrap
import binascii
import optparse

# Utility functions

def rgbToHex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def hexToRgb(hexmsg):
    return tuple(int(i, 16) for i in textwrap.wrap(hexmsg[1:], 2))
    #return tuple(map(ord, hexmsg[1:].decode('hex')))
    
def strToBin(strmsg):
    binmsg = bin(int(binascii.hexlify(strmsg.encode()), 16))
    return binmsg[2:]
    
def binToStr(binmsg):
    strmsg = binascii.unhexlify('%x' % (int('0b' + binmsg, 2)))
    return strmsg
    
def textEncode(hexmsg, digit):
    if hexmsg[-1] in ('0', '1', '2', '3', '4', '5'):
        hexmsg = hexmsg[:-1] + digit
        return hexmsg
    else:
        return None

def textDecode(hexmsg):
    if hexmsg[-1] in ('0', '1'):
        return hexmsg[-1]
    else:
        return None
        
# Main functions

def textHide(imgfilename, msg):
    img = Image.open(imgfilename)
    binmsg = strToBin(msg) + "1111111111111110"
    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        # Stores all the RGB pixels of the image in an array
        imgdata = img.getdata()
        
        newdata = []
        digit = 0
        temp = ''
        
        for pixel in imgdata:
            if digit < len(binmsg):
                newpixel = textEncode(rgbToHex(pixel[0], \
                pixel[1], pixel[2]), binmsg[digit])
                if newpixel == None:
                    newdata.append(pixel)
                else:
                    r, g, b = hexToRgb(newpixel)
                    newdata.append((r, g, b, 255))
                    digit += 1
            else:
                newdata.append(pixel)
            img.putdata(newdata)
            img.save(imgfilename, "PNG")
            return "Text hide completed."
    return "Incompatible image mode, could not hide."
    
def textRetr(imgfilename):
    img = Image.open(imgfilename)
    binmsg = ''
    
    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        imgdata = img.getdata()
        
        for pixel in imgdata:
            digit = textDecode(rghToHex(pixel[0], \
                    pixel[1], pixel[2]))
            if digit == None:
                pass
            else:
                binmsg = binmsg + digit
                if (binmsg[-16:] == "1111111111111110"):
                    print("Decode finished.")
                    return binToStr(binmsg[-16:])
        return binToStr(binmsg)
    return "Incorrect Image mode, could not retrieve."
    
def Main():
    parser = optparse.OptionParser("usage %prog "+"-e/-d <filename>")
    parser.add_option('-e', dest='textHide', type='string', \
                      help='target picture path to hide text')
    parser.add_option('-d', dest='textRetr', type='string', \
                      help='target picture path to retrieve text')
    (options, args) = parser.parse_args()
    
    if (options.textHide != None):s
        text = input("Enter a message to hide: ")
        print(textHide(options.textHide, text))
    elif (options.textRetr != None):
        print(textRetr(options.textRetr))
    else:
        print(parser.usage)
        
if __name__ == '__main__':
    Main()
