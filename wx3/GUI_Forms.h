///////////////////////////////////////////////////////////////////////////
// C++ code generated with wxFormBuilder (version Oct 26 2018)
// http://www.wxformbuilder.org/
//
// PLEASE DO *NOT* EDIT THIS FILE!
///////////////////////////////////////////////////////////////////////////

#pragma once

#include <wx/artprov.h>
#include <wx/xrc/xmlres.h>
#include <wx/string.h>
#include <wx/bitmap.h>
#include <wx/image.h>
#include <wx/icon.h>
#include <wx/menu.h>
#include <wx/gdicmn.h>
#include <wx/font.h>
#include <wx/colour.h>
#include <wx/settings.h>
#include <wx/statusbr.h>
#include <wx/treectrl.h>
#include <wx/sizer.h>
#include <wx/panel.h>
#include <wx/splitter.h>
#include <wx/grid.h>
#include <wx/textctrl.h>
#include <wx/choice.h>
#include <wx/toolbar.h>
#include <wx/frame.h>
#include <wx/stattext.h>
#include <wx/button.h>
#include <wx/dialog.h>

///////////////////////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////////////////////////
/// Class MyFrame1
///////////////////////////////////////////////////////////////////////////////
class MyFrame1 : public wxFrame
{
	private:

	protected:
		wxMenuBar* m_menubar1;
		wxMenu* m_menu1;
		wxMenu* m_menu3;
		wxMenu* m_menu5;
		wxMenu* m_menu6;
		wxMenu* m_menu61;
		wxMenu* m_menu7;
		wxStatusBar* m_statusBar1;
		wxSplitterWindow* m_splitter1;
		wxPanel* m_panel1;
		wxTreeCtrl* m_treeCtrl1;
		wxPanel* m_panel2;
		wxSplitterWindow* m_splitter5;
		wxPanel* m_panel3;
		wxGrid* m_grid1;
		wxTextCtrl* m_textCtrl2;
		wxToolBar* m_toolBar1;
		wxChoice* m_choice1;
		wxToolBarToolBase* m_tool1;
		wxToolBarToolBase* m_tool2;
		wxToolBarToolBase* m_tool3;
		wxToolBarToolBase* m_tool4;

	public:

		MyFrame1( wxWindow* parent, wxWindowID id = wxID_ANY, const wxString& title = wxT("LATTICEMECH2"), const wxPoint& pos = wxDefaultPosition, const wxSize& size = wxSize( 1275,776 ), long style = wxDEFAULT_FRAME_STYLE|wxBORDER_SIMPLE|wxTAB_TRAVERSAL );

		~MyFrame1();

		void m_splitter1OnIdle( wxIdleEvent& )
		{
			m_splitter1->SetSashPosition( 150 );
			m_splitter1->Disconnect( wxEVT_IDLE, wxIdleEventHandler( MyFrame1::m_splitter1OnIdle ), NULL, this );
		}

		void m_splitter5OnIdle( wxIdleEvent& )
		{
			m_splitter5->SetSashPosition( 0 );
			m_splitter5->Disconnect( wxEVT_IDLE, wxIdleEventHandler( MyFrame1::m_splitter5OnIdle ), NULL, this );
		}

};

///////////////////////////////////////////////////////////////////////////////
/// Class target_dialog
///////////////////////////////////////////////////////////////////////////////
class target_dialog : public wxDialog
{
	private:

	protected:
		wxStaticText* m_staticText2;
		wxTextCtrl* m_textCtrl2;
		wxButton* OkButton;
		wxButton* CancelButton;

	public:

		target_dialog( wxWindow* parent, wxWindowID id = wxID_ANY, const wxString& title = wxT("E Target Dialog"), const wxPoint& pos = wxDefaultPosition, const wxSize& size = wxSize( 241,123 ), long style = wxDEFAULT_DIALOG_STYLE );
		~target_dialog();

};

///////////////////////////////////////////////////////////////////////////////
/// Class MeshGeneratorDialog
///////////////////////////////////////////////////////////////////////////////
class MeshGeneratorDialog : public wxDialog
{
	private:

	protected:
		wxStaticText* m_staticText2;
		wxTextCtrl* m_textCtrl3;
		wxButton* OkButtonMesh;
		wxButton* CancelButtonMesh;

	public:

		MeshGeneratorDialog( wxWindow* parent, wxWindowID id = wxID_ANY, const wxString& title = wxT("Mesh generator dialog"), const wxPoint& pos = wxDefaultPosition, const wxSize& size = wxSize( 219,145 ), long style = wxDEFAULT_DIALOG_STYLE );
		~MeshGeneratorDialog();

};

