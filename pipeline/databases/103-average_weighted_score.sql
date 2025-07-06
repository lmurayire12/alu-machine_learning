-- Creates a procedure that computes and updates the average weighted score for a user
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE weighted_sum FLOAT DEFAULT 0;
    DECLARE weight_total INT DEFAULT 0;
    DECLARE avg_score FLOAT DEFAULT 0;

    -- Compute weighted sum and total weights
    SELECT
        SUM(c.score * p.weight),
        SUM(p.weight)
    INTO weighted_sum, weight_total
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    -- Calculate average if weights exist, else 0
    IF weight_total > 0 THEN
        SET avg_score = weighted_sum / weight_total;
    ELSE
        SET avg_score = 0;
    END IF;

    -- Update user's average_score
    UPDATE users
    SET average_score = ROUND(avg_score)
    WHERE id = user_id;
END $$

DELIMITER ;

