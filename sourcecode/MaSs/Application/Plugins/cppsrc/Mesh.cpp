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

				if (!isSubdivide)
				{
					ExportPlyMesh(mesh, exportPath, mesh.GetFullName() + L".ply", isSolid);
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

	void Mesh::ExportPlyMesh(X3DObject& obj, CString exportPath, CString fileName, bool isSolid)
	{
		ofstream f(CUtils::BuildPath(exportPath, fileName).GetAsciiString(), ios::out | ios::binary);

		f << "ply" << endl;
		f << "format ascii 1.0" << endl;

		Geometry oGeom = obj.GetActivePrimitive().GetGeometry();
		CTriangleRefArray tris = oGeom.GetTriangles();
		int vertexcount = tris.GetCount() * 3;
		f << "element vertex " + to_string(vertexcount) << endl;
		f << "property float32 x" << endl;
		f << "property float32 y" << endl;
		f << "property float32 z" << endl;

		if (!isSolid)
		{
			f << "property float32 nx" << endl;
			f << "property float32 ny" << endl;
			f << "property float32 nz" << endl;
		}

		CGeometryAccessor ga = PolygonMesh(oGeom).GetGeometryAccessor();
		CRefArray sUVs = ga.GetUVs();
		LONG uvCount = sUVs.GetCount();

		ClusterProperty uvProp;
		CFloatArray uvValues;

		if (!isSolid && uvCount > 0)
		{
			uvProp = sUVs[0];
			uvProp.GetValues(uvValues);

			f << "property float32 s" << endl;
			f << "property float32 t" << endl;
		}

		CTriangleRefArray triangles = obj.GetActivePrimitive().GetGeometry().GetTriangles();
		int trianglecount = triangles.GetCount();
		f << "element face " + to_string(trianglecount) << endl;
		f << "property list uint8 int32 vertex_index" << endl;
		f << "end_header" << endl;

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

				f << oVertexPos.GetX();
				f << " ";
				f << oVertexPos.GetY();
				f << " ";
				f << oVertexPos.GetZ();
				f << " ";

				//app.LogMessage(L"Position " + CString(i + j) + ": " + CString(oVertexPos.GetX()) + L", " + CString(oVertexPos.GetY()) + L", " + CString(oVertexPos.GetZ()));
				if (!isSolid)
				{
					MATH::CVector3 oVertexNormal = oVertex.GetNormal();

					f << oVertexNormal.GetX();
					f << " ";
					f << oVertexNormal.GetY();
					f << " ";
					f << oVertexNormal.GetZ();
					f << " ";
					//app.LogMessage(L"Normal: "+ CString(oVertexNormal.GetX())+L", "+CString(oVertexNormal.GetY())+L", "+CString(oVertexNormal.GetZ()));

					if (uvCount > 0)
					{
						int nodeId = triNodeIds[i * 3 + j];
						float u = uvValues[nodeId * 3 + 0];
						float v = 1 - uvValues[nodeId * 3 + 1];

						//app.LogMessage(L"u: "+ CString(u));
						//app.LogMessage(L"v: "+ CString(v));

						f << u;
						f << " ";
						f << v;
					}
				}
				f << endl;
				//app.LogMessage(L"clsArray[nCls][(i*3+2)-j]: "+CString(clsArray[nCls][2]));
			}
		}

		for (int i = 0; i < triangles.GetCount(); i++)
		{
			XSI::Triangle triangle(triangles.GetItem(i));
			if (!triangle.IsValid()) continue;

			f << "3 ";
			f << triangle.GetIndex() * 3;
			f << " ";
			f << triangle.GetIndex() * 3 + 1;
			f << " ";
			f << triangle.GetIndex() * 3 + 2;
			f << endl;
		}

		f.close();
	}
}

namespace std
{
	ofstream& operator<<(ofstream& a_stream, const char* a_str)
	{
		if (a_str)
		{
			size_t len = ::strlen(a_str);
			if (len > 0)
				a_stream.write(a_str, len + 1);
		}

		return a_stream;
	}
}
