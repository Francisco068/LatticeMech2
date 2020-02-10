import wx
from wx import glcanvas
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.ARB.shader_objects import *
from OpenGL.GL.ARB.fragment_shader import *
from OpenGL.GL.ARB.vertex_shader import *
import numpy as np

vertexSource = """
#version 130
in vec2 position;
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
}
"""
fragmentSource = """
#version 130
out vec4 outColor;
void main()
{
    outColor = vec4(1.0, 1.0, 1.0, 1.0);
}
"""

class OpenGLCanvas(glcanvas.GLCanvas):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1, size=(640, 480))
        self.init = False
        self.context = glcanvas.GLContext(self) 
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnEraseBackground(self, event):
        pass # Do nothing, to avoid flashing on MSW.

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    def InitGL(self):

        # Vertex Input
        ## Vertex Array Objects
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)

        ## Vertex Buffer Object
        vbo = glGenBuffers(1) # Generate 1 buffer

        vertices = np.array([0.0,  0.5, 0.5, -0.5, -0.5, -0.5], dtype=np.float32)

        ## Upload data to GPU
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # Compile shaders and combining them into a program
        ## Create and compile the vertex shader
        vertexShader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertexShader, vertexSource)
        glCompileShader(vertexShader)

        ## Create and compile the fragment shader
        fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragmentShader, fragmentSource)
        glCompileShader(fragmentShader)

        ## Link the vertex and fragment shader into a shader program
        shaderProgram = glCreateProgram()
        glAttachShader(shaderProgram, vertexShader)
        glAttachShader(shaderProgram, fragmentShader)
        glBindFragDataLocation(shaderProgram, 0, "outColor")
        glLinkProgram(shaderProgram)
        glUseProgram(shaderProgram)

        # Making the link between vertex data and attributes
        posAttrib = glGetAttribLocation(shaderProgram, "position")
        glEnableVertexAttribArray(posAttrib)
        glVertexAttribPointer(posAttrib, 2, GL_FLOAT, GL_FALSE, 0, None)

    def OnDraw(self):
        # Set clear color
        glClearColor(0.0, 0.0, 0.0, 1.0)
    #Clear the screen to black
        glClear(GL_COLOR_BUFFER_BIT)

        # draw six faces of a cube
        glDrawArrays(GL_TRIANGLES, 0, 3)

        self.SwapBuffers()

class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Hello World", size=(640,480))
        canvas = OpenGLCanvas(self)

app = wx.App()
frame = Frame()
frame.Show()
app.MainLoop()