from django import forms
from .models import PTRRequest, MachineModel, TypeOfMachine, Department, PartMaster


class PTRRequestForm(forms.Form):
    """PTR / TCMR Request submission form — manually defined to support
    auto-fill fields and dynamic dropdowns via AJAX."""

    UNIT_CHOICES = [
        ("", "-- Select Unit --"),
        ("ASMIPL", "ASMIPL"),
        ("ASYM", "ASYM"),
    ]

    # ── Step 1: Unit selector ──
    unit = forms.ChoiceField(
        choices=UNIT_CHOICES,
        widget=forms.Select(attrs={"class": "form-control form-select", "id": "id_unit"}),
        label="Select Unit",
    )

    # ── Step 2: Department (populated via AJAX) ──
    deptid = forms.IntegerField(
        widget=forms.Select(attrs={"class": "form-control form-select", "id": "id_deptid", "disabled": "disabled"}),
        label="From Department",
    )

    # ── Step 3: Part No (searchable, populated via AJAX) ──
    partid = forms.IntegerField(
        widget=forms.Select(attrs={"class": "form-control form-select", "id": "id_partid", "disabled": "disabled"}),
        label="Part No.",
    )

    # ── Auto-filled fields (read-only) ──
    customer_display = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control", "id": "id_customer_display",
            "readonly": "readonly", "style": "background-color: #f1f5f9; cursor: not-allowed;",
        }),
        label="Customer",
    )
    project_display = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control", "id": "id_project_display",
            "readonly": "readonly", "style": "background-color: #f1f5f9; cursor: not-allowed;",
        }),
        label="Project Name",
    )
    fg_part_name_display = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control", "id": "id_fg_part_name_display",
            "readonly": "readonly", "style": "background-color: #f1f5f9; cursor: not-allowed;",
        }),
        label="FG Part Name",
    )
    partname_display = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control", "id": "id_partname_display",
            "readonly": "readonly", "style": "background-color: #f1f5f9; cursor: not-allowed;",
        }),
        label="Part Name",
    )

    # ── Hidden fields to store actual IDs for submission ──
    customerid = forms.IntegerField(widget=forms.HiddenInput(attrs={"id": "id_customerid"}), required=False)
    projectid = forms.IntegerField(widget=forms.HiddenInput(attrs={"id": "id_projectid"}), required=False)
    partcode = forms.CharField(widget=forms.HiddenInput(attrs={"id": "id_partcode"}), required=False)
    partname = forms.CharField(widget=forms.HiddenInput(attrs={"id": "id_partname"}), required=False)

    # ── Manual entry fields ──
    drawing = forms.CharField(
        max_length=400,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter drawing number"}),
        label="Drawing No.",
    )
    req_path = forms.CharField(
        max_length=1000, required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter draft process & input models path"}),
        label="Draft Process & Input Models Path",
    )

    # ── TCMR checkbox ──
    istcmr = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input", "id": "id_istcmr"}),
        label="TCMR Request",
    )

    # ── Rev / Obsolete (read-only for PTR) ──
    current_rev_no = forms.CharField(
        initial="NA", required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control", "readonly": "readonly",
            "style": "background-color: #f1f5f9; cursor: not-allowed;",
        }),
        label="Current Rev No.",
    )
    last_obsolete_date = forms.CharField(
        initial="NA", required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control", "readonly": "readonly",
            "style": "background-color: #f1f5f9; cursor: not-allowed;",
        }),
        label="Last Obsolete Date",
    )

    # ── Right column fields ──
    dotr = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        label="Date of Tooling Reqd (Project Plan)",
    )
    earlydatereason = forms.CharField(
        max_length=1500, required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter reason"}),
        label="Reason",
    )
    process = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter process name / number"}),
        label="Process Name | No.",
    )
    ncsno = forms.CharField(
        max_length=4000, required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter N.C setup sheet no(s)"}),
        label="N.C Set Up Sheet No(s)",
    )
    bqty = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "0", "min": "0"}),
        label="Qty / Annum",
    )
    mfg = forms.CharField(
        max_length=4000, required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter MR / PFD sheet no(s)"}),
        label="MR / PFD Sheet No(s)",
    )
    requestremarks = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Enter any remarks..."}),
        label="Remarks from Requester",
    )

    # ── Machine dropdowns (populated via AJAX from Admin Entry) ──
    mmodel = forms.CharField(
        required=False,
        widget=forms.Select(attrs={"class": "form-control form-select", "id": "id_mmodel", "disabled": "disabled"}),
        label="Machine Model",
    )
    typemachine = forms.CharField(
        required=False,
        widget=forms.Select(attrs={"class": "form-control form-select", "id": "id_typemachine", "disabled": "disabled"}),
        label="Type of Machine",
    )


class MachineModelForm(forms.ModelForm):
    class Meta:
        model = MachineModel
        fields = ["unit", "model", "description"]
        widgets = {
            "unit": forms.TextInput(attrs={"type": "hidden", "class": "hidden-unit-input"}),
            "model": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter model name...", "required": True}),
            "description": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter description..."}),
        }

class TypeOfMachineForm(forms.ModelForm):
    class Meta:
        model = TypeOfMachine
        fields = ["unit", "type_of_machine", "description"]
        widgets = {
            "unit": forms.TextInput(attrs={"type": "hidden", "class": "hidden-unit-input"}),
            "type_of_machine": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter machine type...", "required": True}),
            "description": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter description..."}),
        }
