#include "Mesh.h"

namespace Mitsuba
{
	Mesh::Mesh(){}
	Mesh::~Mesh(){}


	void Mesh::WriteMeshes(XMLDocument* doc, XMLElement* sceneElement, XSI::X3DObject& mesh, bool shouldExportGeometry, CString filePath)
	{
		if (isVisibility(mesh))
		{
			sceneElement->InsertEndChild(GenerateMeshSegment(doc, mesh, shouldExportGeometry, filePath));
		}
	}

	XMLElement* Mesh::GenerateMeshSegment(XMLDocument* doc, X3DObject& mesh, bool shouldExport, CString exportPath)
	{
		XMLElement* root = nullptr;

		if (MeshIsMassPrimitive(mesh))
		{
			Primitives* primitive = new Primitives();
			root = primitive->WritePrimitive(doc, mesh);
			delete primitive;
		}
		else
		{
			root = doc->NewElement("shape");
			root->SetAttribute(Constants::attrType, "ply");

			root->InsertEndChild(WriteElement(doc, Constants::attrString, Constants::attrFilename, (mesh.GetFullName() + L".ply").GetAsciiString()));

			XMLElement* trElement = doc->NewElement("transform");
			trElement->SetAttribute(Constants::attrName, "toWorld");
			root->InsertEndChild(trElement);

			MATH::CTransformation transform = mesh.GetKinematics().GetGlobal().GetTransform();
			trElement->InsertEndChild(WriteElementScale(doc, mesh));

			trElement->InsertEndChild(WriteSubElementRotation(doc, "x", transform.GetRotX()));
			trElement->InsertEndChild(WriteSubElementRotation(doc, "y", transform.GetRotY()));
			trElement->InsertEndChild(WriteSubElementRotation(doc, "z", transform.GetRotZ()));

			trElement->InsertEndChild(WriteElementTranslate(doc, mesh));

			Mitsuba::Material* material = new Mitsuba::Material();
			material->WriteMeshMaterial(doc, root, mesh);
			delete material;

			if (shouldExport)
			{
				bool isSolid = false;
				bool isSubdivide = false;
				LONG subLevel = 0;

				Property prop;
				mesh.GetPropertyFromName(L"MaSsObjectProperty", prop);
				if (prop.IsValid())
				{
					isSolid = prop.GetParameterValue(L"isSolid");
					isSubdivide = prop.GetParameterValue(L"isSubdivide");
					subLevel = prop.GetParameterValue(L"subLevel");
				}

				if (isSolid)
				{
					if (!isSubdivide)
					{
						ExportPlyMesh02(mesh, exportPath, mesh.GetFullName() + L".ply");
					}
					else
					{
						/*#we should subdivide this mesh and then export
						#lm("We should subdivide the mesh")
						subOps = ap.ApplyOp("MeshSubdivideWithCenter", mesh)
						subMesh = ap.Selection(0)
						subOp = subOps(0)
						ap.SetValue(subOp.SubdivisionDepth, subLevel)
						ap.FreezeObj(subMesh, "", "")

						tM = mesh.Kinematics.Global.Transform.Matrix4
						oTrans = subMesh.Kinematics.Global.Transform
						tM.InvertInPlace()
						oTrans.SetMatrix4(tM)
						subMesh.Kinematics.Global.Transform = oTrans
						ap.ResetTransform(subMesh, "siCtr", "siSRT", "siXYZ")

						ExportPlyMesh02(subMesh, exportPath, mesh.FullName + ".ply")
						ap.DeleteObj(subMesh)*/
					}
				}
				else
				{
					if (!isSubdivide)
					{
						ExportPlyMesh(mesh, exportPath, mesh.GetFullName() + L".ply");
					}
					else
					{
						/*subOps = ap.ApplyOp("MeshSubdivideWithCenter", mesh)
						subMesh = ap.Selection(0)
						subOp = subOps(0)
						ap.SetValue(subOp.SubdivisionDepth, subLevel)
						ap.TransferAllPropertiesAcrossGenOp(subOp, subMesh, "", True, "")

						ap.FreezeObj(subMesh, "", "")
						tM = mesh.Kinematics.Global.Transform.Matrix4
						oTrans = subMesh.Kinematics.Global.Transform
						tM.InvertInPlace()
						oTrans.SetMatrix4(tM)
						subMesh.Kinematics.Global.Transform = oTrans
						ap.ResetTransform(subMesh, "siCtr", "siSRT", "siXYZ")

						ExportPlyMesh(subMesh, exportPath, mesh.FullName + ".ply")
						ap.DeleteObj(subMesh)*/
					}
				}
			}
		}


		return root;
	}

	bool Mesh::MeshIsMassPrimitive(X3DObject& mesh)
	{
		CRefArray props = mesh.GetProperties();
		for (int i = 0; i < props.GetCount(); i++)
		{
			Property prop(props.GetItem(i));
			if (!prop.IsValid()) continue;

			CString propName = prop.GetName();
			propName.Lower();
			if (propName == L"masssphereprimitiveproperty" ||
				propName == L"masscubeprimitiveproperty" ||
				propName == L"masscylinderprimitiveproperty" ||
				propName == L"massrectangleprimitiveproperty" ||
				propName == L"massdiskprimitiveproperty")
			{
				return true;
			}
		}

		return false;
	}

	void Mesh::ExportPlyMesh(X3DObject& obj, CString exportPath, CString fileName)
	{
		ofstream f(CUtils::BuildPath(exportPath, fileName).GetAsciiString(), ios::out | ios::binary);

		f << "ply\n";
		f << "format ascii 1.0\n";

		Geometry oGeom = obj.GetActivePrimitive().GetGeometry();
		CTriangleRefArray tris = oGeom.GetTriangles();
		int vertexcount = tris.GetCount() * 3;
		f << "element vertex " + to_string(vertexcount) + "\n";
		f << "property float32 x\n";
		f << "property float32 y\n";
		f << "property float32 z\n";

		f << "property float32 nx\n";
		f << "property float32 ny\n";
		f << "property float32 nz\n";

		CGeometryAccessor ga = PolygonMesh(oGeom).GetGeometryAccessor();
		CRefArray sUVs = ga.GetUVs();
		if (sUVs.GetCount() > 0)
		{
			f << "property float32 s\n";
			f << "property float32 t\n";
		}

		CTriangleRefArray triangles = obj.GetActivePrimitive().GetGeometry().GetTriangles();
		int trianglecount = triangles.GetCount();
		f << "element face " + to_string(trianglecount) + "\n";
		f << "property list uint8 int32 vertex_index\n";
		f << "end_header\n";

		//app.LogMessage(L"Tris Count: " + CString(triangles.GetCount()));

		CLongArray triNodeIds;
		ga.GetTriangleNodeIndices(triNodeIds);


		for (int i = 0; i < triangles.GetCount(); i++)
		{
			XSI::Triangle triangle(triangles.GetItem(i));

			for (int j = 2; j >= 0; j--)
			{
				CTriangleVertexRefArray vertArray = triangle.GetPoints();
				//app.LogMessage(L"Point Count: " + CString(vertArray.GetCount()));

				//app.LogMessage(L"Point index: " + vertArray.GetItem(j).GetAsText());
				XSI::TriangleVertex oVertex(vertArray.GetItem(j));
				MATH::CVector3 oVertexPos = oVertex.GetPosition();

				f << to_string(oVertexPos.GetX()) + " ";
				f << to_string(oVertexPos.GetY()) + " ";
				f << to_string(oVertexPos.GetZ()) + " ";

				//app.LogMessage(L"Position " + CString(i + j) + ": " + CString(oVertexPos.GetX()) + L", " + CString(oVertexPos.GetY()) + L", " + CString(oVertexPos.GetZ()));

				MATH::CVector3 oVertexNormal = oVertex.GetNormal();

				f << to_string(oVertexNormal.GetX()) + " ";
				f << to_string(oVertexNormal.GetY()) + " ";
				f << to_string(oVertexNormal.GetZ()) + " ";
				//app.LogMessage(L"Normal: "+ CString(oVertexNormal.GetX())+L", "+CString(oVertexNormal.GetY())+L", "+CString(oVertexNormal.GetZ()));

				if (sUVs.GetCount() > 0)
				{
					for (int r = 0; r < 1; r++)
					{
						ClusterProperty uvProp = sUVs[r];
						CFloatArray uvValues;
						uvProp.GetValues(uvValues);
						int nodeId = triNodeIds[i * 3 + j];

						float u = uvValues[nodeId * 3 + 0];
						float v = 1 - uvValues[nodeId * 3 + 1];

						//app.LogMessage(L"u: "+ CString(u));
						//app.LogMessage(L"v: "+ CString(v));

						f << to_string(u) + " ";
						f << to_string(v) + " ";
					}
				}
				f << "\n";
				//app.LogMessage(L"clsArray[nCls][(i*3+2)-j]: "+CString(clsArray[nCls][2]));
			}
		}

		for (int i = 0; i < triangles.GetCount(); i++)
		{
			XSI::Triangle triangle(triangles.GetItem(i));
			if (!triangle.IsValid()) continue;

			f << "3 ";
			f << to_string(triangle.GetIndex() * 3) + " ";
			f << to_string(triangle.GetIndex() * 3 + 1) + " ";
			f << to_string(triangle.GetIndex() * 3 + 2) + " ";
			f << "\n";
		}

		f.close();
	}

	void Mesh::ExportPlyMesh02(X3DObject& obj, CString exportPath, CString fileName)
	{
		ofstream f(CUtils::BuildPath(exportPath, fileName).GetAsciiString(), ios::out | ios::binary);

		f << "ply\n";
		f << "format ascii 1.0\n";

		CPointRefArray points = obj.GetActivePrimitive().GetGeometry().GetPoints();
		int vertexcount = points.GetCount();
		f << "element vertex " + to_string(vertexcount) + "\n";
		f << "property float32 x\n";
		f << "property float32 y\n";
		f << "property float32 z\n";

		CFacetRefArray facets = obj.GetActivePrimitive().GetGeometry().GetFacets();
		int facescount = facets.GetCount();
		f << "element face " + to_string(facescount) + "\n";
		f << "property list uint8 int32 vertex_index\n";
		f << "end_header\n";

		for (int i = 0; i < vertexcount; i++)
		{
			XSI::Point point(points.GetItem(i));
			if (!point.IsValid()) continue;

			f << to_string(point.GetPosition().GetX()) + " " + to_string(point.GetPosition().GetY()) + " " + to_string(point.GetPosition().GetZ()) + "\n";
		}

		for (int i = 0; i < facescount; i++)
		{
			XSI::Facet facet(facets.GetItem(i));
			if (!facet.IsValid()) continue;

			CPointRefArray facePoints = facet.GetPoints();
			f << to_string(facePoints.GetCount()) + " ";

			for (int p = 0; p < facePoints.GetCount(); p++)
			{
				XSI::Point point(facePoints.GetItem(p));
				if (!point.IsValid()) continue;

				f << to_string(point.GetIndex()) + " ";
			}

			f << "\n";
		}

		f.close();
	}

}
