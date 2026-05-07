from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='ptr_app/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("api/dashboard-stats/", views.api_dashboard_stats, name="api_dashboard_stats"),
    
    path("", views.ptr_request_view, name="ptr_request"),
    path("success/", views.ptr_success_view, name="ptr_success"),
    path("manager-approval/", views.manager_approval_view, name="manager_approval"),
    path("ptr-admin/", views.ptr_admin_list_view, name="ptr_admin_list"),
    path("ptr-admin/<int:pk>/", views.ptr_admin_detail_view, name="ptr_admin_detail"),
    path("designer-entry/", views.designer_entry_list_view, name="designer_entry_list"),
    path("designer-entry/<int:req_id>/", views.designer_entry_detail_view, name="designer_entry_detail"),
    path("receiving-entry/", views.receiving_entry_view, name="receiving_entry"),
    path("receiving-entry/<int:req_id>/", views.receiving_entry_detail_view, name="receiving_entry_detail"),
    path("receiving-entry-feedback/", views.receiving_feedback_view, name="receiving_feedback"),
    path("preventive-maintenance/pm-due/export/", views.export_pm_due_excel, name="export_pm_due_excel"),
    path("preventive-maintenance/plan/", views.pm_plan_view, name="pm_plan"),
    path("preventive-maintenance/plan/<int:pk>/", views.pm_plan_detail_view, name="pm_plan_detail"),
    path('preventive-maintenance/breakdown/', views.breakdown_maintenance_view, name="breakdown_maintenance"),
    path('preventive-maintenance/tool-life/', views.tool_life_extension_view, name="tool_life_extension"),
    path('preventive-maintenance/tool-life/<int:pk>/', views.tool_life_extend_detail_view, name="tool_life_extend_detail"),
    path("history-card/<int:pk>/", views.history_card_view, name="history_card"),
    path("tooling-admin/admin-entry/", views.ta_admin_entry_view, name="ta_admin_entry"),
    path("tooling-admin/change-designer/", views.ta_change_designer_view, name="ta_change_designer"),
    path("tooling-admin/supplier-resource/", views.ta_supplier_resource_view, name="ta_supplier_resource"),
    path("tooling-admin/update-material/", views.ta_update_material_view, name="ta_update_material"),
    path("system-admin/design-dashboard/", views.sa_design_dashboard_view, name="sa_design_dashboard"),
    path("system-admin/employee-mapping/", views.sa_employee_mapping_view, name="sa_employee_mapping"),
    path("system-admin/employee-mapping/load/", views.sa_employee_mapping_load, name="sa_employee_mapping_load"),
    path("system-admin/employee-mapping/delete/<str:emp>/", views.sa_delete_employee_mapping, name="sa_delete_employee_mapping"),
    path("system-admin/form-mapping/", views.sa_form_mapping_view, name="sa_form_mapping"),
    path("system-admin/form-mapping/load/", views.sa_form_mapping_load, name="sa_form_mapping_load"),
    path("tooling-admin/admin-entry/view-machine/", views.ta_admin_entry_view_machine, name="ta_admin_entry_view_machine"),
    path("tooling-admin/admin-entry/view-type/", views.ta_admin_entry_view_type, name="ta_admin_entry_view_type"),
    path("tooling-admin/admin-entry/machine/<int:pk>/edit/", views.ta_edit_machine_model, name="ta_edit_machine_model"),
    path("tooling-admin/admin-entry/type/<int:pk>/edit/", views.ta_edit_type_machine, name="ta_edit_type_machine"),
    path("tooling-admin/admin-entry/machine/<int:pk>/delete/", views.ta_delete_machine_model, name="ta_delete_machine_model"),
    path("tooling-admin/admin-entry/type/<int:pk>/delete/", views.ta_delete_type_machine, name="ta_delete_type_machine"),
    path("obsolete-fixtures/", views.obsolete_fixtures_view, name="obsolete_fixtures"),
    path("get-ptrs-by-tino/", views.get_ptrs_by_tino, name="get_ptrs_by_tino"),
    path("short-close/", views.short_close_view, name="short_close"),
    
    path("reports/", views.reports_view, name="reports"),
    path("reports/export/<str:unit>/", views.export_report_excel, name="export_report_excel"),

    # ── Manager Approval actions ──
    path("manager-approval/approve/<int:pk>/", views.approve_request, name="approve_request"),
    path("manager-approval/reject/<int:pk>/", views.reject_request, name="reject_request"),
    path("manager-approval/obsolete/approve/<int:pk>/", views.approve_obsolete_view, name="approve_obsolete"),
    path("manager-approval/edit/<int:pk>/", views.manager_edit_request, name="manager_edit_request"),

    # ── AJAX API endpoints for PTR form ──
    path("api/departments/", views.api_departments, name="api_departments"),
    path("api/parts/", views.api_parts, name="api_parts"),
    path("api/part-detail/", views.api_part_detail, name="api_part_detail"),
    path("api/machines/", views.api_machines, name="api_machines"),
    path("api/tcmr-autofill/", views.api_tcmr_autofill_data, name="api_tcmr_autofill_data"),
    path("api/designers-by-unit/", views.api_designers_by_unit, name="api_designers_by_unit"),
    path("api/ptrs-by-designer/", views.api_ptrs_by_designer, name="api_ptrs_by_designer"),
    path("api/active-ptrs/", views.api_active_ptrs_by_unit, name="api_active_ptrs_by_unit"),
]
