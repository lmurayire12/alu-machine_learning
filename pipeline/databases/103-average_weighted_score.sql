-- Computes and updates the average weighted score for a user in users.average_score

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE weighted_sum FLOAT DEFAULT 0;
    DECLARE total_weight FLOAT DEFAULT 0;
    DECLARE avg_score FLOAT DEFAULT 0;

    -- Compute the sum of weighted scores and the total weight
    SELECT
        SUM(c.score * p.weight),
        SUM(p.weight)
    INTO weighted_sum, total_weight
    FROM corrections c
        INNER JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    -- If the student has any corrections, compute the average
    IF total_weight > 0 THEN
        SET avg_score = weighted_sum / total_weight;
    ELSE
        SET avg_score = 0;
    END IF;

    -- Update the user's average_score (rounded as in sample)
    UPDATE users
    SET average_score = ROUND(avg_score)
    WHERE id = user_id;
END $$
DELIMITER ;

