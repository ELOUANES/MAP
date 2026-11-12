
# رسم الحدود الإدارية
    if boundary_proj is not None:
        for geom in boundary_proj.geometry:
            for poly_coords in process_geom_coords(geom):
                if len(poly_coords) > 2:
                    msp.add_lwpolyline(poly_coords, close=True, dxfattribs={'layer': '01_Boundary'})

    # رسم الشوارع
    for u, v, data in graph_proj.edges(data=True):
        try:
            if 'geometry' in data:
                line_coords = [shift_coord(pt[0], pt[1]) for pt in data['geometry'].coords]
                if len(line_coords) > 1:
                    msp.add_lwpolyline(line_coords, dxfattribs={'layer': '02_Streets'})
            else:
                p1 = shift_coord(graph_proj.nodes[u]['x'], graph_proj.nodes[u]['y'])
                p2 = shift_coord(graph_proj.nodes[v]['x'], graph_proj.nodes[v]['y'])
                msp.add_line(p1, p2, dxfattribs={'layer': '02_Streets'})
        except:
            continue

    # دالة عامة لرسم البنايات والمرافق مع أسمائها
    def draw_features_dataframe(df, layer_name, text_height=10):
        if df is None or df.empty:
            return
        for idx, row in df.iterrows():
            geom = row.geometry
            name = row.get('name', '')
            if geom is not None:
                try:
                    for poly_coords in process_geom_coords(geom):
                        if len(poly_coords) > 2:
                            msp.add_lwpolyline(poly_coords, close=True, dxfattribs={'layer': layer_name})
                    
                    # إضافة النص في المنتصف إذا وجد اسم للمرفق
                    if isinstance(name, str) and name.strip():
                        c = geom.centroid
                        cx, cy = shift_coord(c.x, c.y)
                        msp.add_text(name, dxfattribs={'height': text_height, 'layer': 'Equipment_Names', 'insert': (cx, cy)})
                except:
                    continue

    print("4. رسم البنايات والمرافق المصنفة...")
    draw_features_dataframe(buildings_proj, '03_Buildings', text_height=8)

    layer_mapping = {
        'educational': 'Eq_Educational',
        'health': 'Eq_Health',
        'cultural': 'Eq_Cultural',
        'religious': 'Eq_Religious',
        'administrative': 'Eq_Administrative'
    }

    for cat, layer_name in layer_mapping.items():
        if cat in proj_categorized:
            draw_features_dataframe(proj_categorized[cat], layer_name, text_height=12)

    output_filename = "Bouira_Professional_Map.dxf"
    doc.saveas(output_filename)
    print(f"
تم بنجاح حفظ الملف الاحترافي باسم: {output_filename})
