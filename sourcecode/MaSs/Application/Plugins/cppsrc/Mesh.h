#pragma once

#include <fstream>

#include "tinyxml2.h"
#include "Constants.h"
#include "BaseElement.h"
#include "Primitives.h"
#include "Material.h"

#include "xsi_geometry.h"
#include "xsi_primitive.h"
#include "xsi_point.h"
#include "xsi_facet.h"
#include "xsi_material.h"
#include "xsi_utils.h"
#include "xsi_geometryaccessor.h"
#include "xsi_polygonmesh.h"
#include "xsi_triangle.h"
#include <xsi_trianglevertex.h>
#include "xsi_vertex.h"
#include <xsi_ref.h>
#include <xsi_vector3.h>

namespace Mitsuba
{
	class Mesh : BaseElement
	{
	public:
		Mesh();
		~Mesh();

		void WriteMeshes(XMLDocument* doc, XMLElement* sceneElement, XSI::X3DObject& mesh, bool shouldExportGeometry, CString filePath);

	private:
		XMLElement* GenerateMeshSegment(XMLDocument* doc, X3DObject& mesh, bool shouldExport, CString exportPath);
		bool MeshIsMassPrimitive(X3DObject& mesh);

		void ExportPlyMesh(X3DObject& obj, CString exportPath, CString fileName);
		void ExportPlyMesh02(X3DObject& obj, CString exportPath, CString fileName);
	};
}

