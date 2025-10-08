-- Buat tabel sast_report_userscmprofile
CREATE TABLE sast_report_userscmprofile (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    scm_type VARCHAR(10) NOT NULL,
    access_token VARCHAR(255) NOT NULL,
    api_url VARCHAR(200),
    username VARCHAR(100),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user(id)
);

-- Buat tabel sast_report_repository (dengan description)
CREATE TABLE sast_report_repository (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    repo_id VARCHAR(100) NOT NULL,
    name VARCHAR(200) NOT NULL,
    url VARCHAR(200) NOT NULL,
    private BOOLEAN DEFAULT FALSE,
    default_branch VARCHAR(100) DEFAULT 'main',
    description TEXT,
    last_sync DATETIME NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME NOT NULL,
    scm_profile_id BIGINT NOT NULL,
    FOREIGN KEY (scm_profile_id) REFERENCES sast_report_userscmprofile(id),
    UNIQUE KEY unique_scm_repo (scm_profile_id, repo_id)
);

-- Buat tabel sast_report_scanschedule
CREATE TABLE sast_report_scanschedule (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    frequency VARCHAR(10) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_run DATETIME NULL,
    next_run DATETIME NULL,
    created_at DATETIME NOT NULL,
    repository_id BIGINT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (repository_id) REFERENCES sast_report_repository(id),
    FOREIGN KEY (user_id) REFERENCES auth_user(id)
);

-- Buat tabel sast_report_scanjob
CREATE TABLE sast_report_scanjob (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    branch VARCHAR(100) DEFAULT 'main',
    status VARCHAR(10) DEFAULT 'pending',
    triggered_at DATETIME NOT NULL,
    started_at DATETIME NULL,
    finished_at DATETIME NULL,
    findings_count INT DEFAULT 0,
    critical_count INT DEFAULT 0,
    high_count INT DEFAULT 0,
    medium_count INT DEFAULT 0,
    low_count INT DEFAULT 0,
    info_count INT DEFAULT 0,
    log TEXT,
    scan_duration TIME NULL,
    repository_id BIGINT NOT NULL,
    user_id INT NOT NULL,
    schedule_id BIGINT NULL,
    FOREIGN KEY (repository_id) REFERENCES sast_report_repository(id),
    FOREIGN KEY (user_id) REFERENCES auth_user(id),
    FOREIGN KEY (schedule_id) REFERENCES sast_report_scanschedule(id)
);

-- Buat tabel sast_report_vulnerabilityreport
CREATE TABLE sast_report_vulnerabilityreport (
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
    metadata TEXT DEFAULT '{}',
    is_false_positive BOOLEAN DEFAULT FALSE,
    created_at DATETIME NOT NULL,
    scan_job_id BIGINT NOT NULL,
    FOREIGN KEY (scan_job_id) REFERENCES sast_report_scanjob(id)
);

-- Buat tabel sast_report_dashboardpermission
CREATE TABLE sast_report_dashboardpermission (
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
