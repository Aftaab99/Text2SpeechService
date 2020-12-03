CREATE TABLE Configuration (
    server_id NUMERIC(5) PRIMARY KEY,
    n_cpu NUMERIC(2),
    ram NUMERIC(2),
    gpuavailable BOOLEAN
);

CREATE TABLE PredictionLog (
    server_id NUMERIC(5) REFERENCES Configuration(server_id),
    request_timestamp TIMESTAMP,
    num_words NUMERIC(2) NOT NULL, 
    prediction_time NUMERIC(3) NOT NULL, -- Time taken to synthesize that sentence, in seconds
    sentence_length NUMERIC(3) NOT NULL,
    CONSTRAINT chk_nwords CHECK (num_words>=1 AND num_words<=50),-- Limiting number of words in a sentence to 20
    CONSTRAINT chk_length CHECK (sentence_length<1000), -- and max length to 100 characters
    PRIMARY KEY(server_id, request_timestamp)
);
