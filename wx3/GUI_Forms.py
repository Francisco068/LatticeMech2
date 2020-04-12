# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1275,776 ), style = wx.DEFAULT_FRAME_STYLE|wx.BORDER_SIMPLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menu1 = wx.Menu()
		self.m_menuItem1 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Open", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_menuItem1 )

		self.m_menuItem2 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Save", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_menuItem2 )

		self.m_menuItem3 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Save as", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_menuItem3 )

		self.m_menuItem13 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Export", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_menuItem13 )

		self.m_menuItem4 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Close", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_menuItem4 )

		self.m_menubar1.Append( self.m_menu1, u"File" )

		self.m_menu3 = wx.Menu()
		self.m_menuItem5 = wx.MenuItem( self.m_menu3, wx.ID_ANY, u"Delete item", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu3.Append( self.m_menuItem5 )

		self.m_menubar1.Append( self.m_menu3, u"Edit" )

		self.m_menu5 = wx.Menu()
		self.m_menuItem6 = wx.MenuItem( self.m_menu5, wx.ID_ANY, u"Visu 2D", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu5.Append( self.m_menuItem6 )

		self.m_menuItem7 = wx.MenuItem( self.m_menu5, wx.ID_ANY, u"Visu 3D", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu5.Append( self.m_menuItem7 )

		self.m_menuItem8 = wx.MenuItem( self.m_menu5, wx.ID_ANY, u"Yield limits", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu5.Append( self.m_menuItem8 )

		self.m_menubar1.Append( self.m_menu5, u"View" )

		self.m_menu6 = wx.Menu()
		self.m_menuItem9 = wx.MenuItem( self.m_menu6, wx.ID_ANY, u"Add Point", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu6.Append( self.m_menuItem9 )

		self.m_menuItem10 = wx.MenuItem( self.m_menu6, wx.ID_ANY, u"Add Beam", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu6.Append( self.m_menuItem10 )

		self.m_menubar1.Append( self.m_menu6, u"Tools" )

		self.m_menu61 = wx.Menu()
		self.m_menuItem12 = wx.MenuItem( self.m_menu61, wx.ID_ANY, u"Go", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu61.Append( self.m_menuItem12 )

		self.m_menubar1.Append( self.m_menu61, u"Calculations" )

		self.m_menu7 = wx.Menu()
		self.m_menuItem11 = wx.MenuItem( self.m_menu7, wx.ID_ANY, u"Help", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu7.Append( self.m_menuItem11 )

		self.m_menubar1.Append( self.m_menu7, u"Help" )

		self.SetMenuBar( self.m_menubar1 )

		self.m_statusBar1 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_splitter1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_BORDER )
		self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )

		self.m_panel1 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		self.m_treeCtrl1 = wx.TreeCtrl( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.BORDER_SIMPLE )
		bSizer8.Add( self.m_treeCtrl1, 1, wx.ALL|wx.BOTTOM|wx.FIXED_MINSIZE|wx.EXPAND, 5 )


		self.m_panel1.SetSizer( bSizer8 )
		self.m_panel1.Layout()
		bSizer8.Fit( self.m_panel1 )
		self.m_panel2 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel2.SetMinSize( wx.Size( 100,100 ) )

		bSizer10 = wx.BoxSizer( wx.VERTICAL )

		self.m_splitter5 = wx.SplitterWindow( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter5.Bind( wx.EVT_IDLE, self.m_splitter5OnIdle )

		self.m_panel3 = wx.Panel( self.m_splitter5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_splitter5.Initialize( self.m_panel3 )
		bSizer10.Add( self.m_splitter5, 1, wx.EXPAND, 5 )

		self.m_grid1 = wx.grid.Grid( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.m_grid1.CreateGrid( 1, 5 )
		self.m_grid1.EnableEditing( True )
		self.m_grid1.EnableGridLines( True )
		self.m_grid1.EnableDragGridSize( False )
		self.m_grid1.SetMargins( 0, 0 )

		# Columns
		self.m_grid1.EnableDragColMove( False )
		self.m_grid1.EnableDragColSize( True )
		self.m_grid1.SetColLabelSize( 30 )
		self.m_grid1.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.m_grid1.EnableDragRowSize( True )
		self.m_grid1.SetRowLabelSize( 80 )
		self.m_grid1.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.m_grid1.SetDefaultCellFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
		self.m_grid1.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer10.Add( self.m_grid1, 0, wx.EXPAND, 5 )


		self.m_panel2.SetSizer( bSizer10 )
		self.m_panel2.Layout()
		bSizer10.Fit( self.m_panel2 )
		self.m_splitter1.SplitVertically( self.m_panel1, self.m_panel2, 150 )
		bSizer1.Add( self.m_splitter1, 4, wx.EXPAND, 5 )

		self.m_textCtrl2 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		self.m_textCtrl2.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Courier New" ) )
		self.m_textCtrl2.SetMinSize( wx.Size( -1,150 ) )

		bSizer1.Add( self.m_textCtrl2, 1, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_toolBar1 = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY )
		m_choice1Choices = [ u"visu 3d", u"yield limits", u"visu 2d", wx.EmptyString ]
		self.m_choice1 = wx.Choice( self.m_toolBar1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice1Choices, 0 )
		self.m_choice1.SetSelection( 0 )
		self.m_toolBar1.AddControl( self.m_choice1 )
		self.m_tool1 = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"icone_moins.bmp", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.m_tool2 = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"icone_plus_point.bmp", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.m_tool3 = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"icone_plus_poutre.bmp", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.m_tool4 = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"icone_calculations.bmp", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.m_toolBar1.Realize()


		self.Centre( wx.BOTH )

	def __del__( self ):
		pass

	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 150 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )

	def m_splitter5OnIdle( self, event ):
		self.m_splitter5.SetSashPosition( 0 )
		self.m_splitter5.Unbind( wx.EVT_IDLE )


