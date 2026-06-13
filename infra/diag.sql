SELECT status, COUNT(*) FROM processing_queue GROUP BY status;
SELECT COUNT(*) FROM processing_dlq;
SELECT MAX(attempts) FROM processing_queue;
