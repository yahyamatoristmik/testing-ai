-- Buat vulnerabilityreport table
CREATE TABLE IF NOT EXISTS sast_report_vulnerabilityreport (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    rule_id VARCHAR(200) NOT NULL,
    severity VARCHAR(10) NOT NULL,
    confidence VARCHAR(10) DEFAULT 'MEDIUM',
    file_path VARCHAR(500) NOT NULL,
    line_number INT NOT NULL,
    message TEXT NOT NULL,
    description TEXT NOT NULL,
    recommendation TEXT NOT NULL,
    code_snippet TEXT,
    cwe_id VARCHAR(20),
    owasp_category VARCHAR(100),
    metadata TEXT,
    is_false_positive BOOLEAN DEFAULT FALSE,
    created_at DATETIME NOT NULL,
    scan_job_id BIGINT NOT NULL,
    FOREIGN KEY (scan_job_id) REFERENCES sast_report_scanjob(id)
);

-- Buat dashboardpermission table
CREATE TABLE IF NOT EXISTS sast_report_dashboardpermission (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    can_view_dashboard BOOLEAN DEFAULT TRUE,
    can_trigger_scans BOOLEAN DEFAULT TRUE,
    can_manage_schedules BOOLEAN DEFAULT FALSE,
    can_view_reports BOOLEAN DEFAULT TRUE,
    can_manage_false_positives BOOLEAN DEFAULT FALSE,
    created_at DATETIME NOT NULL,
    group_id INT NOT NULL,
    FOREIGN KEY (group_id) REFERENCES auth_group(id),
    UNIQUE KEY unique_group (group_id)
);
