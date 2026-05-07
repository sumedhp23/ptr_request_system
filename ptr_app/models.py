from django.db import models


UNIT_CHOICES = [
    ("ASMIPL", "ASMIPL"),
    ("ASYM", "ASYM"),
]


# ──────────────────────────── Lookup / Master Tables ──────────────────────────


class Department(models.Model):
    """Department master — maps to tbl_Department."""
    dID = models.AutoField(primary_key=True)
    DeptName = models.CharField(max_length=150, verbose_name="Department Name")
    Deptdesc = models.CharField(max_length=250, blank=True, null=True, verbose_name="Description")
    unit = models.CharField(max_length=50, blank=True, null=True, choices=UNIT_CHOICES)

    class Meta:
        db_table = "tbl_Department"
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return f"{self.DeptName} ({self.unit})"


class Customer(models.Model):
    """Customer master — maps to tbl_Customer."""
    CustID = models.IntegerField(primary_key=True)
    CustomerName = models.CharField(max_length=100, verbose_name="Customer Name")
    CustomerDesc = models.CharField(max_length=150, blank=True, null=True, verbose_name="Description")
    unit = models.CharField(max_length=150, blank=True, null=True, choices=UNIT_CHOICES)

    class Meta:
        db_table = "tbl_Customer"
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.CustomerName


class Project(models.Model):
    """Project master — maps to tbl_Project."""
    PID = models.IntegerField(primary_key=True)
    custid = models.ForeignKey(
        Customer, on_delete=models.CASCADE, db_column="custid",
        verbose_name="Customer"
    )
    prjname = models.CharField(max_length=250, blank=True, null=True, verbose_name="Project Name")
    unit = models.CharField(max_length=100, blank=True, null=True, choices=UNIT_CHOICES)

    class Meta:
        db_table = "tbl_Project"
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return f"{self.prjname} ({self.unit})"


class PartMaster(models.Model):
    """Parts master — maps to tbl_Parts."""
    PartID = models.AutoField(primary_key=True)
    PartName = models.CharField(max_length=150, verbose_name="Part No. / Code")
    PartDesc = models.CharField(max_length=250, blank=True, null=True, verbose_name="Part Description")
    PrjID = models.ForeignKey(
        Project, on_delete=models.CASCADE, db_column="PrjID",
        verbose_name="Project"
    )
    unit = models.CharField(max_length=150, blank=True, null=True, choices=UNIT_CHOICES)

    class Meta:
        db_table = "tbl_Parts"
        verbose_name = "Part"
        verbose_name_plural = "Parts"

    def __str__(self):
        return f"{self.PartName} — {self.PartDesc or ''}"


# ──────────────────────────── PTR Request ─────────────────────────────────────


class PTRRequest(models.Model):
    """Process Tool Request / TCMR Request — maps to production PTR table."""

    # ── Core identifiers ──
    ptrno = models.CharField(max_length=150, blank=True, null=True, verbose_name="PTR Number")
    unit = models.CharField(max_length=150, blank=True, null=True, choices=UNIT_CHOICES)
    deptid = models.IntegerField(default=0, verbose_name="Department ID")
    partid = models.CharField(max_length=200, blank=True, null=True, verbose_name="Part ID")
    partcode = models.CharField(max_length=200, blank=True, null=True, verbose_name="Part Code")
    partname = models.CharField(max_length=50, blank=True, null=True, verbose_name="Part Name")
    customerid = models.IntegerField(default=0, verbose_name="Customer ID")
    projectid = models.IntegerField(default=0, verbose_name="Project ID")

    # ── Form fields (manual entry) ──
    process = models.CharField(max_length=200, verbose_name="Process Name / No.")
    drawing = models.CharField(max_length=400, verbose_name="Drawing No.")
    dotr = models.DateTimeField(verbose_name="Date of Tooling Required")
    ncsno = models.CharField(max_length=4000, blank=True, null=True, verbose_name="NC Setup Sheet No(s)")
    bqty = models.CharField(max_length=50, blank=True, null=True, verbose_name="Batch Qty")
    mfg = models.CharField(max_length=4000, blank=True, null=True, verbose_name="MR / PFD Sheet No(s)")
    requestremarks = models.CharField(max_length=550, blank=True, null=True, verbose_name="Remarks")
    mmodel = models.CharField(max_length=50, blank=True, null=True, verbose_name="Machine Model")
    typemachine = models.CharField(max_length=50, blank=True, null=True, verbose_name="Type of Machine")

    # ── Status and tracking ──
    status = models.IntegerField(default=0, verbose_name="Status")
    createdby = models.CharField(max_length=150, verbose_name="Created By")
    statusremarks = models.CharField(max_length=150, blank=True, null=True, verbose_name="Status Remarks")
    shortclose = models.BooleanField(null=True, blank=True, verbose_name="Short Close")
    cretedDate = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Created Date")
    istcmr = models.BooleanField(null=True, blank=True, verbose_name="Is TCMR")
    req_path = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Draft Process Path")

    # ── Approval fields ──
    mappprovedate = models.DateTimeField(blank=True, null=True, verbose_name="Manager Approve Date")
    earlydatereason = models.CharField(max_length=1500, blank=True, null=True, verbose_name="Early Date Reason")
    aprrovedmanager = models.CharField(max_length=150, blank=True, null=True, verbose_name="Approved Manager")

    # ── Obsolete / Revision ──
    isobsolete = models.BooleanField(null=True, blank=True, verbose_name="Is Obsolete")
    TINOs = models.CharField(max_length=50, blank=True, null=True, verbose_name="TINO(s)")

    class Meta:
        ordering = ["-cretedDate"]
        verbose_name = "PTR Request"
        verbose_name_plural = "PTR Requests"

    def __str__(self):
        return f"PTR-{self.pk:04d} | {self.partcode or ''} | Unit: {self.unit or ''}"


# ──────────────────────────── Admin Entry Models ────────────────────────────


class MachineModel(models.Model):
    """Admin Entry - Machine Model Configuration."""
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES)
    model = models.CharField(max_length=100, verbose_name="Model")
    description = models.CharField(max_length=255, blank=True, verbose_name="Machine Model Description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Machine Model"
        verbose_name_plural = "Machine Models"

    def __str__(self):
        return f"{self.unit} | {self.model}"


class TypeOfMachine(models.Model):
    """Admin Entry - Type of Machine Configuration."""
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES)
    type_of_machine = models.CharField(max_length=100, verbose_name="Type of Machine")
    description = models.CharField(max_length=255, blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Type of Machine"
        verbose_name_plural = "Types of Machine"

    def __str__(self):
        return f"{self.unit} | {self.type_of_machine}"


# ──────────────────────────── Employee Mapping ────────────────────────────


ROLE_CHOICES = [
    ("PTR Requester", "PTR Requester"),
    ("Approver", "Approver"),
    ("Designer", "Designer"),
    ("ToolingExecutive", "Tooling Executive"),
    ("ToolRoom", "Tool Room"),
    ("Admin", "Admin"),
    ("SystemAdmin", "System Admin"),
    ("PM", "PM"),
]


class EmployeeMapping(models.Model):
    """Employee role-unit mapping — maps to tbl_EmployeeMapping."""
    RowId = models.AutoField(primary_key=True)
    EmpNumber = models.CharField(max_length=50, verbose_name="Employee Number")
    EmpMail = models.CharField(max_length=50, blank=True, null=True, verbose_name="Employee Email")
    Status = models.CharField(max_length=50, blank=True, null=True, default="Active", verbose_name="Status")
    Role = models.CharField(max_length=50, blank=True, null=True, choices=ROLE_CHOICES, verbose_name="Role")
    Unit = models.CharField(max_length=50, blank=True, null=True, verbose_name="Unit")
    department = models.CharField(max_length=50, blank=True, null=True, verbose_name="Department")
    AddedBy = models.CharField(max_length=50, blank=True, null=True, verbose_name="Added By")
    DateTime = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Added Date")
    ModifyBy = models.CharField(max_length=50, blank=True, null=True, verbose_name="Modified By")
    ModifyDate = models.DateTimeField(blank=True, null=True, verbose_name="Modified Date")

    class Meta:
        db_table = "tbl_EmployeeMapping"
        verbose_name = "Employee Mapping"
        verbose_name_plural = "Employee Mappings"

    def __str__(self):
        return f"{self.EmpNumber} | {self.Role} | {self.Unit}"


# ──────────────────────────── Form Mapping ────────────────────────────


# Role ID mapping — maps role names to integer IDs for tbl_FormMapping.RolID
ROLE_ID_MAP = {
    "PTR Requester": 1,
    "Approver": 2,
    "Designer": 3,
    "ToolingExecutive": 4,
    "ToolRoom": 5,
    "Admin": 6,
    "SystemAdmin": 7,
    "PM": 8,
}


class FormMaster(models.Model):
    """Form master — maps to tbl_FormMaster. Lists all forms/pages in the system."""
    RowID = models.AutoField(primary_key=True)
    FormName = models.CharField(max_length=50, blank=True, null=True, verbose_name="Form Name")
    FormID = models.IntegerField(verbose_name="Form ID")

    class Meta:
        db_table = "tbl_FormMaster"
        verbose_name = "Form Master"
        verbose_name_plural = "Form Masters"

    def __str__(self):
        return f"{self.FormID} — {self.FormName}"


class FormMapping(models.Model):
    """Form-role mapping — maps to tbl_FormMapping. Controls which roles can access which forms."""
    RowId = models.AutoField(primary_key=True)
    FormID = models.IntegerField(blank=True, null=True, verbose_name="Form ID")
    RolID = models.IntegerField(blank=True, null=True, verbose_name="Role ID")
    IsActive = models.BooleanField(blank=True, null=True, verbose_name="Is Active")
    AddedBy = models.CharField(max_length=50, blank=True, null=True, verbose_name="Added By")
    DateCreated = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Date Created")

    class Meta:
        db_table = "tbl_FormMapping"
        verbose_name = "Form Mapping"
        verbose_name_plural = "Form Mappings"

    def __str__(self):
        return f"Form {self.FormID} → Role {self.RolID} | Active: {self.IsActive}"


# ──────────────────────────── PTR Admin ────────────────────────────


class PtrAdmin(models.Model):
    """PTR Admin assignment — maps to Tbl_ptrAdmin.
    Created when tooling admin assigns a designer to an approved PTR."""
    ptrno = models.CharField(max_length=150, verbose_name="PTR Number")
    desginer = models.CharField(max_length=150, verbose_name="Designer")
    pldstartdate = models.DateTimeField(blank=True, null=True, verbose_name="Planned Start Date")
    pldcompdate = models.DateTimeField(verbose_name="Planned Completion Date")
    remarks = models.CharField(max_length=150, blank=True, null=True, verbose_name="Remarks")
    shortclose = models.BooleanField(blank=True, null=True, verbose_name="Short Close")
    status = models.BooleanField(blank=True, null=True, verbose_name="Status")
    ptr = models.ForeignKey(
        PTRRequest, on_delete=models.CASCADE, db_column="ptrid",
        verbose_name="PTR Request", related_name="admin_entries"
    )
    plannedHour = models.IntegerField(blank=True, null=True, verbose_name="Planned Hours")

    class Meta:
        db_table = "Tbl_ptrAdmin"
        verbose_name = "PTR Admin"
        verbose_name_plural = "PTR Admin Entries"

    def __str__(self):
        return f"{self.ptrno} | Designer: {self.desginer}"


# ──────────────────── Designer Entry (all 3 forms) ─────────────────────


class DesignerEntry(models.Model):
    """All 3 panel forms write to this single table — tbl_designer.
    Form 1: Designer fields (ASD → desremarks + checkboxes).
    Form 2: Tooling Executive fields (mprDate → eddate).
    Form 3: Tool Room / later-stage fields (Tfeedback, bit-flags, etc.)."""

    ptr = models.ForeignKey(
        PTRRequest, on_delete=models.CASCADE, db_column="ptrid",
        verbose_name="PTR Request", related_name="designer_entries"
    )

    # ── Form 1: Designer ──
    ASD = models.DateTimeField(blank=True, null=True, verbose_name="Actual Start Date")
    ACD = models.DateTimeField(blank=True, null=True, verbose_name="Actual Completion Date")
    DescTooling = models.CharField(max_length=150, blank=True, null=True, verbose_name="Description of Tooling")
    TINo = models.CharField(max_length=50, blank=True, null=True, verbose_name="TINO")
    ECost = models.CharField(max_length=50, blank=True, null=True, verbose_name="Estimated Cost")
    Path = models.CharField(max_length=200, blank=True, null=True, verbose_name="Path in CM")
    ToolMaterial = models.CharField(max_length=250, blank=True, null=True, verbose_name="Tool/Fixture Material")
    toollife = models.CharField(max_length=250, blank=True, null=True, verbose_name="Tool Life")
    PMFrequency = models.IntegerField(blank=True, null=True, verbose_name="PM Frequency / yr")
    actualHr = models.IntegerField(blank=True, null=True, verbose_name="Actual Hours")
    desremarks = models.CharField(max_length=500, blank=True, null=True, verbose_name="Designer Remarks")
    isinhous = models.BooleanField(blank=True, null=True, verbose_name="Aequs Inhouse")
    isVoiceSetup = models.BooleanField(blank=True, null=True, verbose_name="Vice Setup")
    chk_jaw = models.BooleanField(blank=True, null=True, verbose_name="Turning Jaw Setup")
    iscmc = models.BooleanField(blank=True, null=True, verbose_name="Critical Spares Required")
    cmpath = models.CharField(max_length=600, blank=True, null=True, verbose_name="CM Path")

    # ── Form 2: Tooling Executive ──
    mprDate = models.DateTimeField(blank=True, null=True, verbose_name="MPR Date")
    MPRNo = models.CharField(max_length=50, blank=True, null=True, verbose_name="MPR Number")
    suplier = models.CharField(max_length=150, blank=True, null=True, verbose_name="Supplier")
    pocost = models.CharField(max_length=200, blank=True, null=True, verbose_name="Actual Cost as per PO")
    eddate = models.DateField(blank=True, null=True, verbose_name="Expected Delivery Date")
    consumablecode = models.CharField(max_length=200, blank=True, null=True, verbose_name="Fixed Asset Code")
    roino = models.CharField(max_length=300, blank=True, null=True, verbose_name="ROI / WBS")
    waitingroi = models.BooleanField(blank=True, null=True, verbose_name="Waiting for ROI No.")

    # ── Form 3: Tool Room (later stage) ──
    Tfeedback = models.CharField(max_length=200, blank=True, null=True, verbose_name="Trial Feedback Report No.")
    tvdate = models.DateTimeField(blank=True, null=True, verbose_name="TV Date")
    bitfinance = models.BooleanField(blank=True, null=True)
    bitSCM = models.BooleanField(blank=True, null=True)
    biterp = models.BooleanField(blank=True, null=True)
    bitCM = models.BooleanField(blank=True, null=True)
    bitvreport = models.BooleanField(blank=True, null=True)
    bitTfeedback = models.BooleanField(blank=True, null=True)
    statusFeedBack = models.CharField(max_length=200, blank=True, null=True)
    pathtomaster = models.CharField(max_length=300, blank=True, null=True)
    erpcode = models.CharField(max_length=200, blank=True, null=True)
    bitcommon = models.BooleanField(blank=True, null=True)
    commonremarks = models.CharField(max_length=250, blank=True, null=True)
    commonptrid = models.IntegerField(blank=True, null=True)
    latereason = models.CharField(max_length=400, blank=True, null=True)

    # ── Status & tracking ──
    status = models.BooleanField(default=False, verbose_name="Status")
    ToolLifeModifiedBy = models.CharField(max_length=50, blank=True, null=True)
    ToolLifeModifiedDate = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "tbl_designer"
        verbose_name = "Designer Entry"
        verbose_name_plural = "Designer Entries"

    def __str__(self):
        return f"DesignerEntry ptr_id={self.ptr_id}"


class CriticalSpares(models.Model):
    """Critical spares linked to a PTR — tbl_CriticalSpares."""
    TINO = models.CharField(max_length=950, blank=True, null=True, verbose_name="TINO")
    drgNO = models.CharField(max_length=950, blank=True, null=True, verbose_name="Drawing Number")
    cmcode = models.CharField(max_length=950, blank=True, null=True, verbose_name="Consumable Code")
    ptr = models.ForeignKey(
        PTRRequest, on_delete=models.CASCADE, db_column="ptrid",
        blank=True, null=True, verbose_name="PTR Request", related_name="critical_spares"
    )
    mprno = models.CharField(max_length=550, blank=True, null=True, verbose_name="MPR No")
    desc = models.CharField(max_length=950, blank=True, null=True, verbose_name="Description")
    qty = models.IntegerField(blank=True, null=True, verbose_name="Quantity")
    UOM = models.CharField(max_length=250, blank=True, null=True, verbose_name="UOM")

    class Meta:
        db_table = "tbl_CriticalSpares"
        verbose_name = "Critical Spare"
        verbose_name_plural = "Critical Spares"

    def __str__(self):
        return f"Spare ptr_id={self.ptr_id} drgNO={self.drgNO}"


# ──────────────────── Receiving Entry ─────────────────────


class ReceivingEntry(models.Model):
    """Tool receiving record — tbl_receiving.
    Created when tooling exec form is complete and tool is received."""
    ptr = models.ForeignKey(
        PTRRequest, on_delete=models.CASCADE, db_column="ptrid",
        verbose_name="PTR Request", related_name="receiving_entries"
    )
    rcvdate = models.DateTimeField(verbose_name="Receiving Date")
    tvrn = models.CharField(max_length=250, verbose_name="Tooling Verification Report Number")
    grndate = models.DateTimeField(blank=True, null=True, verbose_name="GRN Date")
    grnno = models.CharField(max_length=500, blank=True, null=True, verbose_name="GRN Number")
    ModifiedBy = models.CharField(max_length=30, blank=True, null=True, verbose_name="Modified By")
    ModifiedDate = models.DateTimeField(blank=True, null=True, verbose_name="Modified Date")
    Approver = models.IntegerField(blank=True, null=True, verbose_name="Approver")

    class Meta:
        db_table = "tbl_receiving"
        verbose_name = "Receiving Entry"
        verbose_name_plural = "Receiving Entries"

    def __str__(self):
        return f"Receiving ptr_id={self.ptr_id} tvrn={self.tvrn}"


# ──────────────────── Obsolete Fixtures / Revisions ─────────────────────


class TblRevision(models.Model):
    """Obsolete Fixtures & Revisions — maps to tbl_revision."""
    ptr = models.ForeignKey(
        PTRRequest, on_delete=models.CASCADE, db_column="ptrid",
        verbose_name="PTR Request", related_name="revisions"
    )
    revisionNo = models.IntegerField(default=0, verbose_name="Revision Number")
    DescriptionRev = models.CharField(max_length=500, blank=True, null=True, verbose_name="Reason For Obsolete")
    Approver = models.CharField(max_length=250, blank=True, null=True, verbose_name="Approver")
    Vdate = models.DateField(blank=True, null=True, verbose_name="Approval Date")
    ToolMod = models.CharField(max_length=500, blank=True, null=True, verbose_name="Tool Modification")
    isapproved = models.BooleanField(blank=True, null=True, verbose_name="Is Approved")
    RemarksDisposition = models.CharField(max_length=500, blank=True, null=True, verbose_name="Remarks on Disposition")

    class Meta:
        db_table = "tbl_revision"
        verbose_name = "Revision"
        verbose_name_plural = "Revisions"

    def __str__(self):
        return f"Rev {self.revisionNo} | ptr_id={self.ptr_id}"


# ──────────────────── Preventive Maintenance ─────────────────────


class PreventM(models.Model):
    """Preventive Maintenance record — maps to tbl_preventM."""
    pmdate = models.DateField(verbose_name="Plan Date for Inspection")
    pmreportno = models.CharField(max_length=150, verbose_name="Report No.")
    ptr = models.ForeignKey(
        PTRRequest, on_delete=models.CASCADE, db_column="ptrid",
        verbose_name="PTR Request", related_name="preventative_maintenances"
    )
    actualdate = models.DateField(verbose_name="Actual Date")
    rmk = models.CharField(max_length=250, verbose_name="Remarks")
    inspector = models.CharField(max_length=250, null=True, blank=True, verbose_name="Inspector")
    Approver = models.CharField(max_length=250, null=True, blank=True, verbose_name="Approver")
    status = models.CharField(max_length=50, null=True, blank=True, verbose_name="Status")
    TINO = models.CharField(max_length=250, null=True, blank=True, verbose_name="TINO")
    
    class Meta:
        db_table = "tbl_preventM"
        verbose_name = "Preventive Maintenance"
        verbose_name_plural = "Preventive Maintenances"

    def __str__(self):
        return f"PM {self.pmreportno} | ptr_id={self.ptr_id}"


# ──────────────────── Breakdown Maintenance ─────────────────────


class Breakdown(models.Model):
    """Breakdown Maintenance record — maps to tbl_breakdown."""
    ptr = models.ForeignKey(
        PTRRequest, on_delete=models.CASCADE, db_column="ptrid",
        verbose_name="PTR Request", related_name="breakdowns"
    )
    Tino = models.CharField(max_length=500, null=True, blank=True, verbose_name="TINO")
    bd_date = models.DateField(null=True, blank=True, verbose_name="Breakdown Date")
    reason = models.CharField(max_length=500, null=True, blank=True, verbose_name="Reason")
    reportNo = models.CharField(max_length=250, null=True, blank=True, verbose_name="Report No")
    Status = models.CharField(max_length=50, null=True, blank=True, verbose_name="Status")
    downtime = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, verbose_name="Downtime")
    Approved = models.CharField(max_length=50, null=True, blank=True, verbose_name="Approved By")
    
    class Meta:
        db_table = "tbl_breakdown"
        verbose_name = "Breakdown Maintenance"
        verbose_name_plural = "Breakdown Maintenances"

    def __str__(self):
        return f"{self.reportNo} | {self.Tino}"


# ──────────────────── Tool Life Extension ─────────────────────


class ToolLifeExtend(models.Model):
    """Tool Life Extension record — maps to Tbl_ToolLifeExtend."""
    RowID = models.AutoField(primary_key=True)
    PTRNo = models.CharField(max_length=50, null=True, blank=True)
    PTRId = models.ForeignKey(PTRRequest, on_delete=models.CASCADE, db_column="PTRId", related_name="tool_extensions")
    TiNo = models.CharField(max_length=50)
    ToolMaterial = models.CharField(max_length=250, null=True, blank=True)
    InspectionReportNo = models.CharField(max_length=50)
    PreviousToolExpiryDate = models.DateTimeField(null=True, blank=True)
    ToolLifeExtendedYr = models.IntegerField()
    ExtendedOn = models.DateTimeField()
    Remarks = models.CharField(max_length=500, null=True, blank=True)
    ApprovedBy = models.CharField(max_length=50, null=True, blank=True)
    InspectedBy = models.CharField(max_length=50, null=True, blank=True)
    Status = models.CharField(max_length=50, null=True, blank=True)
    Unit = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        db_table = "Tbl_ToolLifeExtend"
        verbose_name = "Tool Life Extension"
        verbose_name_plural = "Tool Life Extensions"

    def __str__(self):
        return f"{self.PTRNo} | {self.TiNo}"
