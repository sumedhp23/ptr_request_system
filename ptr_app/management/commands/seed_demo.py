"""
Management command to seed demo data into all lookup tables.
Run:   python3 manage.py seed_demo
Clear: python3 manage.py seed_demo --clear
"""
from django.core.management.base import BaseCommand
from ptr_app.models import Department, Customer, Project, PartMaster, MachineModel, TypeOfMachine


class Command(BaseCommand):
    help = "Seed demo data into lookup tables (Department, Customer, Project, Parts, MachineModel, TypeOfMachine)"

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true", help="Remove all demo data instead of adding it")

    def handle(self, *args, **options):
        if options["clear"]:
            self._clear()
        else:
            self._seed()

    def _clear(self):
        """Delete ALL rows from lookup tables."""
        counts = {
            "Parts": PartMaster.objects.all().delete()[0],
            "Projects": Project.objects.all().delete()[0],
            "Customers": Customer.objects.all().delete()[0],
            "Departments": Department.objects.all().delete()[0],
            "MachineModels": MachineModel.objects.all().delete()[0],
            "TypeOfMachine": TypeOfMachine.objects.all().delete()[0],
        }
        for name, count in counts.items():
            self.stdout.write(self.style.WARNING(f"  Deleted {count} rows from {name}"))
        self.stdout.write(self.style.SUCCESS("\n✓ All demo data cleared."))

    def _seed(self):
        """Insert demo rows into all lookup tables."""

        # ═══════════ DEPARTMENTS ═══════════
        depts = [
            ("Tool Engineering", "Tool Engineering Department", "ASMIPL"),
            ("Production", "Production Department", "ASMIPL"),
            ("Quality", "Quality Assurance Department", "ASMIPL"),
            ("Design", "Design Department", "ASMIPL"),
            ("Maintenance", "Maintenance Department", "ASMIPL"),
            ("Purchase", "Purchase Department", "ASMIPL"),
            ("Tool Engineering", "Tool Engineering Department", "ASYM"),
            ("Production", "Production Department", "ASYM"),
            ("Quality", "Quality Assurance Department", "ASYM"),
            ("Design", "Design Department", "ASYM"),
            ("Maintenance", "Maintenance Department", "ASYM"),
            ("Purchase", "Purchase Department", "ASYM"),
        ]
        for name, desc, unit in depts:
            Department.objects.get_or_create(DeptName=name, unit=unit, defaults={"Deptdesc": desc})
        self.stdout.write(self.style.SUCCESS(f"  ✓ {len(depts)} Departments seeded"))

        # ═══════════ CUSTOMERS ═══════════
        customers_data = [
            (1, "Tata Motors", "Tata Motors Ltd", "ASMIPL"),
            (2, "Mahindra & Mahindra", "Mahindra Auto Division", "ASMIPL"),
            (3, "Bajaj Auto", "Bajaj Auto Ltd", "ASMIPL"),
            (4, "Ashok Leyland", "Ashok Leyland Commercial", "ASMIPL"),
            (5, "Maruti Suzuki", "Maruti Suzuki India Ltd", "ASYM"),
            (6, "Hyundai Motors", "Hyundai Motor India", "ASYM"),
            (7, "Kia India", "Kia India Pvt Ltd", "ASYM"),
            (8, "Toyota Kirloskar", "Toyota Kirloskar Motor", "ASYM"),
        ]
        for cid, name, desc, unit in customers_data:
            Customer.objects.get_or_create(CustID=cid, defaults={"CustomerName": name, "CustomerDesc": desc, "unit": unit})
        self.stdout.write(self.style.SUCCESS(f"  ✓ {len(customers_data)} Customers seeded"))

        # ═══════════ PROJECTS ═══════════
        projects_data = [
            (101, 1, "Nexon EV Platform", "ASMIPL"),
            (102, 1, "Harrier Chassis", "ASMIPL"),
            (103, 2, "XUV700 Body Shell", "ASMIPL"),
            (104, 3, "Pulsar Engine Block", "ASMIPL"),
            (105, 4, "Dost Axle Assembly", "ASMIPL"),
            (201, 5, "Brezza Front Bumper", "ASYM"),
            (202, 5, "Swift Dashboard", "ASYM"),
            (203, 6, "Creta Transmission", "ASYM"),
            (204, 7, "Seltos Door Panel", "ASYM"),
            (205, 8, "Fortuner Frame", "ASYM"),
        ]
        for pid, custid, name, unit in projects_data:
            cust = Customer.objects.get(CustID=custid)
            Project.objects.get_or_create(PID=pid, defaults={"custid": cust, "prjname": name, "unit": unit})
        self.stdout.write(self.style.SUCCESS(f"  ✓ {len(projects_data)} Projects seeded"))

        # ═══════════ PARTS ═══════════
        parts_data = [
            ("G252-74151-204", "Bracket Assembly LH", 101, "ASMIPL"),
            ("G252-74152-205", "Bracket Assembly RH", 101, "ASMIPL"),
            ("H310-55200-100", "Cross Member Front", 102, "ASMIPL"),
            ("H310-55201-101", "Cross Member Rear", 102, "ASMIPL"),
            ("M700-82100-300", "Side Panel Inner LH", 103, "ASMIPL"),
            ("M700-82101-301", "Side Panel Inner RH", 103, "ASMIPL"),
            ("BJ-EN-4400-010", "Cylinder Head Cover", 104, "ASMIPL"),
            ("BJ-EN-4401-011", "Crankcase Lower", 104, "ASMIPL"),
            ("AL-AX-7700-050", "Rear Axle Housing", 105, "ASMIPL"),
            ("AL-AX-7701-051", "Differential Carrier", 105, "ASMIPL"),
            ("MS-BR-1100-001", "Bumper Reinforcement", 201, "ASYM"),
            ("MS-BR-1101-002", "Fog Lamp Bracket", 201, "ASYM"),
            ("MS-DB-2200-010", "Instrument Panel Base", 202, "ASYM"),
            ("MS-DB-2201-011", "Glove Box Frame", 202, "ASYM"),
            ("HY-TR-3300-020", "Transmission Case LH", 203, "ASYM"),
            ("HY-TR-3301-021", "Gear Shift Fork", 203, "ASYM"),
            ("KI-DP-4400-030", "Door Inner Panel LH", 204, "ASYM"),
            ("KI-DP-4401-031", "Window Regulator Bracket", 204, "ASYM"),
            ("TY-FR-5500-040", "Frame Side Rail LH", 205, "ASYM"),
            ("TY-FR-5501-041", "Frame Cross Member #3", 205, "ASYM"),
        ]
        for pname, pdesc, prjid, unit in parts_data:
            prj = Project.objects.get(PID=prjid)
            PartMaster.objects.get_or_create(PartName=pname, PrjID=prj, defaults={"PartDesc": pdesc, "unit": unit})
        self.stdout.write(self.style.SUCCESS(f"  ✓ {len(parts_data)} Parts seeded"))

        # ═══════════ MACHINE MODELS ═══════════
        machine_models_data = [
            ("ASMIPL", "VMC 850", "Vertical Machining Center 850mm"),
            ("ASMIPL", "HMC 630", "Horizontal Machining Center 630mm"),
            ("ASMIPL", "CNC Lathe 200", "CNC Lathe 200mm Chuck"),
            ("ASMIPL", "SPM 100", "Special Purpose Machine 100"),
            ("ASYM", "VMC 1060", "Vertical Machining Center 1060mm"),
            ("ASYM", "HMC 800", "Horizontal Machining Center 800mm"),
            ("ASYM", "CNC Lathe 350", "CNC Lathe 350mm Chuck"),
            ("ASYM", "Grinding M400", "Grinding Machine 400mm"),
        ]
        for unit, model, desc in machine_models_data:
            MachineModel.objects.get_or_create(unit=unit, model=model, defaults={"description": desc})
        self.stdout.write(self.style.SUCCESS(f"  ✓ {len(machine_models_data)} Machine Models seeded"))

        # ═══════════ TYPE OF MACHINE ═══════════
        machine_types_data = [
            ("ASMIPL", "VMC", "Vertical Machining Center"),
            ("ASMIPL", "HMC", "Horizontal Machining Center"),
            ("ASMIPL", "CNC Lathe", "CNC Lathe Machine"),
            ("ASMIPL", "SPM", "Special Purpose Machine"),
            ("ASYM", "VMC", "Vertical Machining Center"),
            ("ASYM", "HMC", "Horizontal Machining Center"),
            ("ASYM", "CNC Lathe", "CNC Lathe Machine"),
            ("ASYM", "Grinding", "Grinding Machine"),
        ]
        for unit, typ, desc in machine_types_data:
            TypeOfMachine.objects.get_or_create(unit=unit, type_of_machine=typ, defaults={"description": desc})
        self.stdout.write(self.style.SUCCESS(f"  ✓ {len(machine_types_data)} Machine Types seeded"))

        self.stdout.write(self.style.SUCCESS("\n✓ All demo data seeded successfully!"))
