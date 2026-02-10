# Peepl HR Custom - HR Recruitment Module

## Overview

Peepl HR Custom is a comprehensive Odoo 19 module that extends the standard HR Recruitment functionality with advanced assessment tracking, dynamic custom fields, and interactive dashboards. This module is designed to streamline the recruitment process by providing detailed candidate evaluation tools and real-time analytics.

**Key Highlights:**
- 🎯 Automated candidate assessment and validation
- 📊 Real-time interactive dashboard with charts
- 🔧 Dynamic custom fields without coding
- 📈 Multi-view reporting (Kanban, List, Graph, Pivot)
- 🔒 Stage locking for rejected candidates
- ⚡ Inline editing for bulk updates

## Table of Contents

- [Quick Start Guide](#quick-start-guide)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Recruitment Workflow](#recruitment-workflow)
  - [Managing Candidates](#managing-candidates)
  - [Using the Dashboard](#using-the-dashboard)
  - [Working with Custom Fields](#working-with-custom-fields)
- [Module Structure](#module-structure)
- [Technical Details](#technical-details)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [License](#license)

---

## Quick Start Guide

### For First-Time Users

1. **Install the Module**
   - Go to Apps → Search "Peepl HR Custom" → Click Install
   - Wait for installation to complete (automatic database setup)

2. **Configure Basic Settings**
   - Navigate to Recruitment → Configuration
   - Review Test Results, Phases, and Status configurations
   - Add custom fields if needed (optional)

3. **Add Your First Candidate**
   - Go to Recruitment → Applications → New
   - Fill in Name, Email, Job Position, Contract Type
   - Go to Assessment tab → Enter test scores
   - System automatically validates and sets status

4. **View Dashboard**
   - Navigate to Recruitment → Dashboard
   - See real-time KPIs, charts, and candidate list
   - Use filters to analyze data

### Typical Workflow

```
1. Candidate Application
   ↓
2. Enter Assessment Scores (VGR, NGR, LAG, CHE, BEI, VCR, NCR)
   ↓
3. Select Contract Type (Staff/Supervisor/Manager)
   ↓
4. System Auto-Validates Requirements
   ↓
5. Set Recruitment Phase (Online Test → AI Interview → User Interview → PSC Interview)
   ↓
6. Make Hire Decision (On Progress → Recommended → Offer Made / Do Not Pursue)
   ↓
7. Track Progress in Dashboard
```

---

## Features

### 1. **Assessment Tracking System**

Track comprehensive candidate assessments with predefined test scores:

- **VGR (Verbal General Reasoning)** - Numeric score
- **NGR (Numerical General Reasoning)** - Numeric score
- **LAG (Logical Abstract General)** - Numeric score
- **CHE (Checking)** - Numeric score
- **BEI (Behavioral Event Interview)** - Selection (A1, A2, B1, B2, C1, C2)
- **VCR (Verbal Critical Reasoning)** - Numeric score
- **NCR (Numerical Critical Reasoning)** - Numeric score

### 2. **Recruitment Phase Management**

Track candidates through different recruitment stages:

- Online Test Failed
- Online Test Passed
- AI Interview
- User Interview
- PSC Interview

### 3. **Hire Decision Tracking**

Monitor hiring decisions with status indicators:

- **On Progress** - Candidate is being evaluated
- **Recommended** - Candidate is recommended for hire
- **Offer Made** - Job offer has been extended
- **Do Not Pursue** - Candidate is rejected (locks stage changes)

### 4. **Auto-Validation System**

Automatic validation based on contract type requirements:

#### Staff Requirements:
- VGR, NGR, LAG ≥ 5
- CHE ≥ 7
- BEI = B1, B2, C1, or C2
- VCR, NCR ≥ 4

#### Supervisor/Manager Requirements:
- VGR, NGR, LAG ≥ 6
- CHE ≥ 8
- BEI = B1, B2, C1, or C2
- VCR, NCR ≥ 6

### 5. **Dynamic Custom Fields**

Create unlimited custom fields for hr.applicant without code:

- **Supported Field Types:**
  - Text (Single line)
  - Multiline Text
  - Integer
  - Decimal/Float
  - Checkbox/Boolean
  - Date
  - DateTime
  - Dropdown/Selection
  - Many2one (Relational)

- **Features:**
  - Drag & drop sequence ordering
  - Auto-inject into list and form views
  - Optional visibility in list view
  - Real-time field creation without restart
  - Automatic database column management

### 6. **Interactive Dashboard**

Real-time recruitment analytics with:

- **KPI Cards:**
  - Total Applicants
  - Assessed Candidates
  - On Progress Count
  - Do Not Pursue Count

- **Interactive Charts:**
  - Recruitment Phases (Pie Chart)
  - Hire Decisions (Pie Chart)
  - Click-to-filter functionality

- **Advanced Data Table:**
  - Search functionality
  - Multi-filter options (Phase, Decision, Month)
  - Sortable columns
  - Pagination (10/20/50/100 rows)
  - Dynamic custom field columns
  - Export-ready data view

### 7. **Enhanced Views**

- **Kanban View** - Visual candidate pipeline grouped by phase
- **List View** - Editable inline grid with all assessment fields
- **Form View** - Comprehensive candidate profile with assessment tab
- **Graph View** - Pie charts for phase and decision analysis
- **Pivot View** - Cross-tabulation of phases and decisions

### 8. **Configuration Management**

Centralized configuration for:

- **Test Results** - Manage test types and scoring
- **Recruitment Phases** - Define custom phases
- **Recruitment Status** - Configure status options
- **Custom Fields** - Create dynamic fields

---

## Installation

### Prerequisites

- Odoo 19.0 or higher
- Python 3.10+
- PostgreSQL 12+

### Dependencies

This module depends on:
- `base` - Odoo base module
- `hr_recruitment` - Standard HR Recruitment
- `hr_recruitment_reports` - Recruitment reporting
- `hr_contract` - For contract type validation

### Installation Steps

1. **Copy Module to Addons Path**
   ```bash
   cp -r peepl_hr_custom /path/to/odoo/addons/
   ```

2. **Update Apps List**
   - Go to Apps menu
   - Click "Update Apps List"
   - Search for "Peepl HR Custom"

3. **Install Module**
   - Click "Install" button
   - Wait for installation to complete

4. **Verify Installation**
   - Check Recruitment menu for new Dashboard option
   - Verify Configuration menu has new items

---

## Configuration

### Initial Setup

#### 1. Configure Test Results

Navigate to: **Recruitment > Configuration > Test Results**

- Add or modify test types (VGR, NGR, LAG, etc.)
- Set sequence for display order
- Activate/deactivate tests as needed

#### 2. Configure Recruitment Phases

Navigate to: **Recruitment > Configuration > Recruitment Phases**

- Define custom recruitment phases
- Set sequence for workflow order
- Manage active/inactive phases

#### 3. Configure Recruitment Status

Navigate to: **Recruitment > Configuration > Recruitment Status**

- Define hiring decision statuses
- Customize status names
- Set display sequence

#### 4. Create Custom Fields

Navigate to: **Recruitment > Configuration > Custom Fields**

**To Create a New Field:**

1. Click "New" (or edit existing)
2. Enter Field Name (e.g., "Priority Level")
3. Select Field Type
4. Set Sequence (for ordering)
5. For Selection type: Enter options (one per line)
6. For Many2one type: Enter model name (e.g., res.partner)
7. Click "Save & Reload"
8. Page will refresh and field appears in views

**Field Type Examples:**

- **Text**: Short answers (e.g., "Referral Source")
- **Multiline Text**: Long descriptions (e.g., "Interview Notes")
- **Integer**: Whole numbers (e.g., "Years of Experience")
- **Decimal**: Numbers with decimals (e.g., "Expected Salary")
- **Checkbox**: Yes/No values (e.g., "Willing to Relocate")
- **Date**: Date picker (e.g., "Available Start Date")
- **DateTime**: Date and time (e.g., "Interview Scheduled")
- **Dropdown**: Predefined options (e.g., "Education Level")
- **Many2one**: Link to other records (e.g., "Referred By")

---

## Usage

### Managing Candidates

#### Adding a New Candidate

1. Go to **Recruitment > Applications**
2. Click "New"
3. Fill in basic information:
   - Name
   - Email
   - Job Position
   - Contract Type
4. Go to "Assessment" tab
5. Enter test scores (VGR, NGR, LAG, etc.)
6. System auto-validates based on contract type
7. Set Recruitment Phase and Hire Decision

#### Bulk Editing Candidates

1. Go to **Recruitment > Applications**
2. Switch to List View
3. Edit directly in the grid (inline editing)
4. All fields are editable including custom fields
5. Changes save automatically

#### Using the Dashboard

Navigate to: **Recruitment > Dashboard**

**Dashboard Features:**

1. **KPI Overview**
   - View total applicants at a glance
   - Monitor assessed vs unassessed candidates
   - Track progress and rejections

2. **Interactive Charts**
   - Click on chart segments to filter data
   - View distribution by phase or decision
   - Hover for detailed percentages

3. **Data Table Filters**
   - **Search**: Type name or email to find candidates
   - **Month Filter**: View candidates by test date
   - **Phase Filter**: Filter by recruitment phase
   - **Status Filter**: Filter by hire decision
   - **Rows Per Page**: Choose 10, 20, 50, or 100 rows
   - **Pagination**: Navigate through pages

4. **Sorting**
   - Click "Name ↕" to sort alphabetically
   - Toggle ascending/descending order

### Working with Custom Fields

#### Viewing Custom Fields

Custom fields automatically appear in:

- **List View**: After NCR column (optional visibility)
- **Form View**: In Assessment Scores group (after NCR)
- **Dashboard**: As additional table columns

#### Editing Custom Field Values

1. Open candidate record
2. Go to Assessment tab
3. Scroll to custom fields section
4. Enter values based on field type
5. Save record

#### Managing Custom Fields

**To Edit a Field:**
1. Go to Configuration > Custom Fields
2. Click on field to edit
3. Modify name, type, or options
4. Click "Save & Reload"
5. Page refreshes with changes

**To Delete a Field:**
1. Open field record
2. Click "Action" > "Delete"
3. Confirm deletion
4. Page auto-refreshes
5. Field removed from all views and database

**To Reorder Fields:**
1. Go to Configuration > Custom Fields
2. Drag handle icon to reorder
3. New sequence applies immediately

### Validation Rules

#### Automatic Validation

When you enter assessment scores and select a contract type:

1. System calculates if candidate meets requirements
2. "Meets Requirements" field updates automatically
3. Hire Decision auto-sets based on validation:
   - ✅ Meets requirements → "On Progress"
   - ❌ Doesn't meet → "Do Not Pursue"

#### Stage Lock

When Hire Decision = "Do Not Pursue":
- Stage/Phase cannot be changed
- Prevents accidental progression
- Error message displays if attempted

### Reporting

#### Recruitment Progress Report

Navigate to: **Recruitment > Reporting > Recruitment Progress**

Available views:
- **Kanban**: Visual pipeline
- **List**: Detailed grid
- **Graph**: Pie charts
- **Pivot**: Cross-tabulation
- **Form**: Individual records

#### Exporting Data

From List View:
1. Select records (or select all)
2. Click "Action" > "Export"
3. Choose fields to export
4. Download as CSV/Excel

---

## Module Structure

```
peepl_hr_custom/
├── __init__.py                 # Module initialization
├── __manifest__.py             # Module manifest
├── models/
│   ├── __init__.py
│   ├── hr_applicant.py         # Extended hr.applicant model
│   ├── recruitment_config.py   # Configuration models
│   └── recruitment_custom_field.py  # Dynamic field system
├── views/
│   ├── hr_applicant_views.xml  # Applicant views
│   ├── recruitment_config_views.xml  # Config views
│   ├── recruitment_custom_field_views.xml  # Custom field views
│   └── recruitment_dashboard_views.xml  # Dashboard action
├── static/
│   └── src/
│       ├── css/
│       │   ├── list_view.css
│       │   └── recruitment_dashboard.css
│       ├── js/
│       │   └── recruitment_dashboard.js  # OWL component
│       └── xml/
│           └── recruitment_dashboard.xml  # Dashboard template
├── security/
│   └── ir.model.access.csv     # Access rights
├── data/
│   └── recruitment_test_config_data.xml  # Default data
└── README.md                   # This file
```

---

## Technical Details

### Models

#### 1. hr.applicant (Inherited)

**New Fields:**
- `last_test` (Date) - Date of online test
- `vgr` (Float) - VGR score
- `ngr` (Float) - NGR score
- `lag` (Float) - LAG score
- `che` (Float) - CHE score
- `bei` (Selection) - BEI level
- `vcr` (Float) - VCR score
- `ncr` (Float) - NCR score
- `recruitment_phase` (Selection) - Current phase
- `hire_decision` (Selection) - Hiring decision
- `contract_type_id` (Many2one) - Contract type
- `meets_staff_requirements` (Boolean, Computed) - Validation result
- `total_score` (Float, Computed) - Average score

**Methods:**
- `_compute_staff_requirements()` - Auto-validate scores
- `_compute_total_score()` - Calculate average
- `write()` - Override to prevent stage changes

#### 2. recruitment.custom.field

**Fields:**
- `name` (Text) - Field name
- `sequence` (Integer) - Display order
- `active` (Boolean) - Active status
- `field_type` (Selection) - Field type
- `selection_values` (Text) - Options for dropdown
- `relation_model` (Char) - Model for Many2one

**Methods:**
- `_column_name()` - Generate field name (x_field{id}_value)
- `_sync_template_column()` - Create/update database column
- `create()` - Sync field on creation
- `write()` - Sync field on update
- `unlink()` - Remove field on deletion
- `action_refresh_page()` - Reload page action

#### 3. hr.applicant (Mixin)

**Methods:**
- `fields_get()` - Override to set custom field labels
- `_get_view()` - Intercept view rendering
- `_patch_view()` - Inject custom fields into views

### Database Schema

#### Post-Init Hook

Automatically creates columns on installation:
```sql
ALTER TABLE hr_applicant ADD COLUMN IF NOT EXISTS vgr NUMERIC;
ALTER TABLE hr_applicant ADD COLUMN IF NOT EXISTS ngr NUMERIC;
ALTER TABLE hr_applicant ADD COLUMN IF NOT EXISTS lag NUMERIC;
ALTER TABLE hr_applicant ADD COLUMN IF NOT EXISTS che NUMERIC;
ALTER TABLE hr_applicant ADD COLUMN IF NOT EXISTS bei VARCHAR;
ALTER TABLE hr_applicant ADD COLUMN IF NOT EXISTS vcr NUMERIC;
ALTER TABLE hr_applicant ADD COLUMN IF NOT EXISTS ncr NUMERIC;
ALTER TABLE hr_applicant ADD COLUMN IF NOT EXISTS recruitment_phase VARCHAR;
ALTER TABLE hr_applicant ADD COLUMN IF NOT EXISTS hire_decision VARCHAR;
ALTER TABLE hr_applicant ADD COLUMN IF NOT EXISTS contract_type_id INTEGER;
ALTER TABLE hr_applicant ADD COLUMN IF NOT EXISTS meets_staff_requirements BOOLEAN;
ALTER TABLE hr_applicant ADD COLUMN IF NOT EXISTS total_score NUMERIC;
```

#### Dynamic Field Columns

Custom fields create columns dynamically:
```sql
ALTER TABLE hr_applicant ADD COLUMN x_field{id}_value {type};
CREATE INDEX idx_hr_applicant_x_field{id}_value ON hr_applicant(x_field{id}_value);
```

### Frontend Architecture

#### OWL Component (recruitment_dashboard.js)

**State Management:**
- `loading` - Loading indicator
- `stats` - KPI statistics
- `phaseData` - Phase chart data
- `statusData` - Status chart data
- `recentCandidates` - All candidates
- `filteredCandidates` - Filtered results
- `customFields` - Dynamic field definitions
- `searchText` - Search query
- `filters` - Active filters
- `pagination` - Pagination state

**Key Methods:**
- `loadData()` - Fetch candidates and custom fields
- `filterCandidates()` - Apply filters and search
- `renderCharts()` - Render Chart.js visualizations
- `onChartClick()` - Handle chart interactions
- `getPaginatedCandidates()` - Get current page data

### Security

**Access Rights:**

| Model | User | Manager |
|-------|------|---------|
| recruitment.test.config | Read/Write | Read/Write |
| recruitment.phase.config | Read/Write | Read/Write |
| recruitment.status.config | Read/Write | Read/Write |
| recruitment.custom.field | Read | Full Access |

### Performance Considerations

1. **Indexing**: Custom fields auto-create indexes
2. **Lazy Loading**: Dashboard loads data on demand
3. **Pagination**: Limits records per page
4. **Caching**: Registry cache for field definitions
5. **Computed Fields**: Stored for faster access

---

## Troubleshooting

### Common Issues

#### 1. Custom Fields Not Appearing

**Problem**: Created custom field but not visible in views

**Solution:**
- Click "Save & Reload" button in form
- Clear browser cache (Ctrl+F5)
- Restart Odoo server if needed
- Check field is Active

#### 2. Dashboard Not Loading

**Problem**: Dashboard shows loading spinner indefinitely

**Solution:**
- Check browser console for errors
- Verify Chart.js is loaded
- Check user has access rights
- Restart Odoo server

#### 3. Validation Not Working

**Problem**: Meets Requirements not calculating

**Solution:**
- Ensure Contract Type is selected
- Enter all required scores
- Check contract type name contains "staff", "spv", "supervisor", or "manager"
- Save record to trigger computation

#### 4. Stage Cannot Be Changed

**Problem**: Cannot change recruitment stage

**Solution:**
- Check Hire Decision is not "Do Not Pursue"
- Change Hire Decision first
- Then change stage

#### 5. Custom Field Deletion Error

**Problem**: Error when deleting custom field

**Solution:**
- Ensure no records have data in that field
- Or accept data loss
- Field will be removed from database

### Debug Mode

Enable debug mode for troubleshooting:

1. Go to Settings
2. Activate Developer Mode
3. Check Technical menu for:
   - Database Structure
   - Fields
   - Views

### Logs

Check Odoo logs for errors:
```bash
tail -f /var/log/odoo/odoo-server.log
```

---

## Best Practices

### 1. Custom Field Naming

- Use clear, descriptive names
- Avoid special characters
- Keep names concise for table display
- Use consistent naming convention

### 2. Field Type Selection

- Use Integer for whole numbers
- Use Float for decimals
- Use Selection for limited options
- Use Many2one for relationships
- Use Text for short inputs
- Use Multiline for long text

### 3. Data Entry

- Enter all assessment scores before validation
- Select contract type early
- Use consistent BEI values
- Fill Date of Online Test for filtering

### 4. Dashboard Usage

- Use filters to narrow results
- Export data regularly for backup
- Monitor KPIs weekly
- Click charts for quick filtering

### 5. Performance

- Limit custom fields to necessary ones
- Archive old candidates regularly
- Use pagination for large datasets
- Export and archive historical data

---

## Roadmap

### Planned Features

- [ ] Email notifications for status changes
- [ ] Automated interview scheduling
- [ ] Integration with assessment platforms
- [ ] Advanced reporting with filters
- [ ] Candidate comparison tool
- [ ] Mobile-responsive dashboard
- [ ] Bulk import from CSV
- [ ] Custom validation rules
- [ ] Workflow automation
- [ ] API endpoints for integrations

---

## Support

For issues, questions, or feature requests:

- **Email**: support@peepl.com
- **Website**: https://peepl.com
- **Documentation**: https://docs.peepl.com

---

## License

This module is licensed under LGPL-3.

```
Peepl HR Custom - HR Recruitment Module
Copyright (C) 2024 Peepl

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
```

---

## Credits

**Author**: Peepl  
**Website**: https://peepl.com  
**Version**: 19.0.1.0.3  
**Category**: HR/Projects  

**Contributors**:
- Peepl Development Team

**Special Thanks**:
- Odoo Community
- Chart.js Team
- OWL Framework Team

---

## Changelog

### Version 19.0.1.0.3 (Current)
- ✅ Dynamic custom fields system
- ✅ Interactive dashboard with charts
- ✅ Auto-validation based on contract type
- ✅ Enhanced views (Kanban, List, Form, Graph, Pivot)
- ✅ Stage locking for rejected candidates
- ✅ Comprehensive configuration options
- ✅ Real-time field injection
- ✅ Advanced filtering and search
- ✅ Pagination support
- ✅ Export functionality

### Version 19.0.1.0.2
- Assessment tracking system
- Recruitment phase management
- Hire decision tracking
- Basic configuration

### Version 19.0.1.0.1
- Initial release
- Basic hr.applicant extension

---

**Last Updated**: January 2026  
**Odoo Version**: 19.0+e.20250918  
**Module Name**: peepl_hr_custom
