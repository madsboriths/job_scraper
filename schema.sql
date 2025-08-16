CREATE TABLE IF NOT EXISTS nodes (
  entity TEXT PRIMARY KEY,
  type TEXT,
  count INT
);

CREATE TABLE IF NOT EXISTS edges (
  a TEXT,
  b TEXT,
  count INT,
  PRIMARY KEY (a, b)
);

CREATE TABLE IF NOT EXISTS processed_jobs (
  job_id       TEXT NOT NULL,
  version      TEXT NOT NULL,
  PRIMARY KEY (job_id, version)
);