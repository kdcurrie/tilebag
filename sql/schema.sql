CREATE TABLE words (
	word_id SERIAL PRIMARY KEY,
	word TEXT NOT NULL UNIQUE,
	word_length INT NOT NULL,
	nwl23_is_valid BOOLEAN NOT NULL,
	created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE definitions (
	definition_id SERIAL PRIMARY KEY,
	word_id INT NOT NULL REFERENCES words(word_id),
	definition_source TEXT NOT NULL,
	rank INT NOT NULL,
	definition TEXT NOT NULL,
	part_of_speech TEXT NOT NULL,
	created_at TIMESTAMP DEFAULT NOW(),

	CONSTRAINT unique_word_rank UNIQUE (word_id, definition_source, rank)
);