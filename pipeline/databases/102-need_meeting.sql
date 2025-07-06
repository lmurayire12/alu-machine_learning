-- Creates a view need_meeting that lists all students with score < 80
-- AND (no last_meeting OR last_meeting is more than 1 month ago)

CREATE OR REPLACE VIEW need_meeting AS
SELECT name
FROM students
WHERE score < 80
  AND (
    last_meeting IS NULL
    OR last_meeting < CURDATE() - INTERVAL 1 MONTH
  );

