import framebuf

def pbm_to_framebuf(file):
    with open(file, 'rb') as f:
        if not f.readline() == b'P4\n': return
        f.readline()
        w, h = f.readline().decode().split(' ')
        w = int(w)
        h = int(h.strip())

        return framebuf.FrameBuffer(bytearray(f.readline()),128,64,framebuf.MONO_HLSB)


