# Repository Map: ngram/app

*Generated: 2025-12-23 18:42*

## Statistics

- **Files:** 26
- **Directories:** 12
- **Total Size:** 95.4K
- **Doc Files:** 0
- **Code Files:** 26
- **Areas:** 17 (docs/ subfolders)
- **Modules:** 44 (subfolders in areas)
- **DOCS Links:** 21 (0.81 avg per code file)

### By Language

- tsx: 13
- typescript: 11
- css: 2

## File Tree

```
├── api/ (9.7K)
│   ├── connectome/ (6.3K)
│   │   ├── graph/ (1.7K)
│   │   │   └── route.ts (1.7K)
│   │   ├── graphs/ (1.6K)
│   │   │   └── route.ts (1.6K) →
│   │   └── search/ (3.0K)
│   │       └── route.ts (3.0K)
│   └── sse/ (3.4K)
│       └── route.ts (3.4K)
├── connectome/ (84.9K)
│   ├── components/ (71.3K)
│   │   ├── edge_kit/ (8.5K)
│   │   │   ├── connectome_edge_label_renderer_with_halo_and_zoom_policy.tsx (937) →
│   │   │   ├── connectome_edge_style_tokens_for_trigger_and_calltype_mapping.ts (907) →
│   │   │   ├── connectome_node_boundary_intersection_geometry_helpers.ts (961) →
│   │   │   ├── semantic_edge_components_with_directional_shine_and_pulses.tsx (4.9K) →
│   │   │   └── (..2 more files)
│   │   ├── node_kit/ (14.1K)
│   │   │   ├── connectome_energy_badge_bucketed_glow_and_value_formatter.tsx (811) →
│   │   │   ├── connectome_node_background_theme_tokens_by_type_and_language.ts (1.3K) →
│   │   │   ├── connectome_node_frame_with_title_path_and_tooltip_shell.tsx (1.2K) →
│   │   │   ├── connectome_node_step_list_and_active_step_highlighter.tsx (1.3K) →
│   │   │   ├── connectome_player_wait_progress_bar_with_four_second_cap.tsx (2.0K) →
│   │   │   ├── connectome_tick_cron_circular_progress_ring_with_speed_label.tsx (2.4K) →
│   │   │   └── typed_connectome_node_components_with_energy_and_step_highlighting.tsx (5.1K) →
│   │   ├── connectome_health_panel.tsx (3.9K) →
│   │   ├── connectome_log_duration_formatting_and_threshold_color_rules.ts (808) →
│   │   ├── connectome_log_export_buttons_using_state_store_serializers.tsx (1.3K) →
│   │   ├── connectome_log_trigger_and_calltype_badge_color_tokens.ts (1.1K) →
│   │   ├── connectome_page_shell_route_layout_and_control_surface.tsx (10.9K) →
│   │   ├── deterministic_zone_and_node_layout_computation_helpers.ts (3.5K) →
│   │   ├── edge_label_declutter_and_visibility_policy_helpers.ts (898) →
│   │   ├── pannable_zoomable_zoned_flow_canvas_renderer.tsx (19.9K) →
│   │   └── unified_now_and_copyable_ledger_log_panel.tsx (6.5K) →
│   ├── connectome.css (13.3K)
│   └── (..1 more files)
├── ngram/ (216)
│   └── (..1 more files)
└── globals.css (1.9K)
```

## File Details

### `api/connectome/graph/route.ts`

**Definitions:**
- `runGraphFetch()`
- `GET()`

### `api/connectome/graphs/route.ts`

**Docs:** `docs/connectome/graphs/OBJECTIVES_Connectome_Graphs.md`

**Definitions:**
- `runListGraphs()`
- `GET()`

### `api/connectome/search/route.ts`

**Definitions:**
- `runSearchWithPython()`
- `runSearch()`
- `GET()`

### `api/sse/route.ts`

**Definitions:**
- `formatEvent()`
- `fetchDoctorHealth()`
- `GET()`

### `connectome/components/edge_kit/connectome_edge_label_renderer_with_halo_and_zoom_policy.tsx`

**Docs:** `docs/connectome/edge_kit/IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md`

### `connectome/components/edge_kit/connectome_edge_style_tokens_for_trigger_and_calltype_mapping.ts`

**Docs:** `docs/connectome/edge_kit/IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md`

**Definitions:**
- `dash_for_trigger()`
- `color_for_call_type()`
- `trigger_label()`

### `connectome/components/edge_kit/connectome_node_boundary_intersection_geometry_helpers.ts`

**Docs:** `docs/connectome/edge_kit/IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md`

**Definitions:**
- `clamp()`
- `intersect_line_with_rect()`

### `connectome/components/edge_kit/semantic_edge_components_with_directional_shine_and_pulses.tsx`

**Docs:** `docs/connectome/edge_kit/IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md`

**Definitions:**
- `EdgeComponent()`
- `strokeWidth()`

### `connectome/components/node_kit/connectome_energy_badge_bucketed_glow_and_value_formatter.tsx`

**Docs:** `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md`

**Definitions:**
- `bucket_for_energy()`

### `connectome/components/node_kit/connectome_node_background_theme_tokens_by_type_and_language.ts`

**Docs:** `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md`

**Definitions:**
- `theme_for_node()`
- `title_color_for_node()`

### `connectome/components/node_kit/connectome_node_frame_with_title_path_and_tooltip_shell.tsx`

**Docs:** `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md`

### `connectome/components/node_kit/connectome_node_step_list_and_active_step_highlighter.tsx`

**Docs:** `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md`

**Definitions:**
- `color_for_call_type()`

### `connectome/components/node_kit/connectome_player_wait_progress_bar_with_four_second_cap.tsx`

**Docs:** `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md`

**Definitions:**
- `color_for_seconds()`

### `connectome/components/node_kit/connectome_tick_cron_circular_progress_ring_with_speed_label.tsx`

**Docs:** `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md`

**Definitions:**
- `color_for_speed()`
- `elapsed()`

### `connectome/components/node_kit/typed_connectome_node_components_with_energy_and_step_highlighting.tsx`

**Docs:** `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md`

**Definitions:**
- `build_node_tooltip()`
- `BaseNode()`
- `renderHint()`
- `PlayerNode()`
- `renderHint()`
- `handleClick()`
- `handleKeyDown()`
- `TickCronNode()`
- `renderHint()`

### `connectome/components/connectome_health_panel.tsx`

**Docs:** `docs/connectome/health/HEALTH_Connectome_Live_Signals.md`

**Definitions:**
- `status_label()`

### `connectome/components/connectome_log_duration_formatting_and_threshold_color_rules.ts`

**Docs:** `docs/connectome/log_panel/IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md`

**Definitions:**
- `duration_text()`
- `duration_class()`

### `connectome/components/connectome_log_export_buttons_using_state_store_serializers.tsx`

**Docs:** `docs/connectome/log_panel/IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md`

**Definitions:**
- `copy_to_clipboard()`
- `handleCopyJsonl()`
- `handleCopyText()`

### `connectome/components/connectome_log_trigger_and_calltype_badge_color_tokens.ts`

**Docs:** `docs/connectome/log_panel/IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md`

**Definitions:**
- `trigger_badge_class()`
- `call_type_badge_class()`

### `connectome/components/connectome_page_shell_route_layout_and_control_surface.tsx`

**Docs:** `docs/connectome/page_shell/PATTERNS_Connectome_Page_Shell_Route_Composition_And_User_Control_Surface_Patterns.md`

**Definitions:**
- `connect()`
- `loadGraphs()`
- `loadGraph()`
- `handleNext()`
- `handleRestart()`
- `handleSpeedChange()`
- `handleModeChange()`
- `handleSearch()`
- `nodeIds()`
- `edgeIds()`

### `connectome/components/deterministic_zone_and_node_layout_computation_helpers.ts`

**Docs:** `docs/connectome/flow_canvas/IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md`

**Definitions:**
- `compute_zones()`
- `compute_node_positions()`

### `connectome/components/edge_label_declutter_and_visibility_policy_helpers.ts`

**Docs:** `docs/connectome/flow_canvas/IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md`

**Definitions:**
- `compute_label_anchors()`

### `connectome/components/pannable_zoomable_zoned_flow_canvas_renderer.tsx`

**Docs:** `docs/connectome/flow_canvas/IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md`

**Definitions:**
- `hex_to_rgb()`
- `build_shader()`
- `build_program()`
- `CanvasInner()`
- `searchNodes()`
- `searchEdges()`
- `searchEdges()`
- `render()`
- `sx()`
- `sy()`
- `handleWheel()`
- `handleMouseDown()`
- `handleMouseMove()`
- `worldX()`
- `worldY()`
- `handleMouseUp()`
- `worldX()`
- `worldY()`

### `connectome/components/unified_now_and_copyable_ledger_log_panel.tsx`

**Docs:** `docs/connectome/log_panel/IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md`

**Definitions:**
- `node_label()`
- `node_class()`
- `call_type_detail()`
- `trigger_detail()`
