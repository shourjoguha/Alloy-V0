--
-- PostgreSQL database dump
--

\restrict Zusjb51QfU1quAagXkcYO27QhN8UsU0Ofqfw0fWSBvvSPjxmCxNmfGPkdpTWiDv

-- Dumped from database version 16.11 (Debian 16.11-1.pgdg13+1)
-- Dumped by pg_dump version 16.11 (Debian 16.11-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: activitycategory; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.activitycategory AS ENUM (
    'STRENGTH',
    'CARDIO',
    'MOBILITY',
    'SPORT',
    'RECOVERY',
    'OTHER'
);


ALTER TYPE public.activitycategory OWNER TO jacked;

--
-- Name: circuittier; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.circuittier AS ENUM (
    'beginner',
    'intermediate',
    'advanced',
    'expert',
    'bronze'
);


ALTER TYPE public.circuittier OWNER TO jacked;

--
-- Name: cnsload; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.cnsload AS ENUM (
    'very_low',
    'low',
    'moderate',
    'high',
    'very_high'
);


ALTER TYPE public.cnsload OWNER TO jacked;

--
-- Name: defaultmetrictype; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.defaultmetrictype AS ENUM (
    'reps',
    'time',
    'time_under_tension',
    'distance',
    'calories',
    'DISTANCE',
    'TIME'
);


ALTER TYPE public.defaultmetrictype OWNER TO jacked;

--
-- Name: disciplinecategory; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.disciplinecategory AS ENUM (
    'TRAINING',
    'SPORT',
    'RECOVERY',
    'OTHER',
    'calisthenics',
    'powerlifting',
    'crossfit',
    'bodybuilding',
    'yoga',
    'strongman',
    'olympic_weightlifting'
);


ALTER TYPE public.disciplinecategory OWNER TO jacked;

--
-- Name: disciplinetype; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.disciplinetype AS ENUM (
    'powerlifting',
    'olympic_weightlifting',
    'bodybuilding',
    'crossfit',
    'strongman',
    'calisthenics',
    'yoga',
    'running',
    'other'
);


ALTER TYPE public.disciplinetype OWNER TO jacked;

--
-- Name: disciplinetype_new; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.disciplinetype_new AS ENUM (
    'resistance training',
    'olympic',
    'crossfit',
    'yoga',
    'running',
    'other'
);


ALTER TYPE public.disciplinetype_new OWNER TO jacked;

--
-- Name: disciplinetype_new2; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.disciplinetype_new2 AS ENUM (
    'resistance training',
    'olympic',
    'crossfit',
    'yoga',
    'mobility',
    'stretch',
    'athletic',
    'running',
    'other'
);


ALTER TYPE public.disciplinetype_new2 OWNER TO jacked;

--
-- Name: disciplinetype_new3; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.disciplinetype_new3 AS ENUM (
    'resistance training',
    'olympic',
    'crossfit',
    'yoga',
    'mobility',
    'stretch',
    'athletic',
    'cardio',
    'running',
    'other'
);


ALTER TYPE public.disciplinetype_new3 OWNER TO jacked;

--
-- Name: exercise_approach_type; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.exercise_approach_type AS ENUM (
    'compound',
    'isolation',
    'dynamic',
    'static',
    'unilateral',
    'bilateral'
);


ALTER TYPE public.exercise_approach_type OWNER TO jacked;

--
-- Name: goaltype; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.goaltype AS ENUM (
    'PERFORMANCE',
    'BODY_COMPOSITION',
    'SKILL',
    'HEALTH',
    'HABIT',
    'OTHER',
    'STRENGTH',
    'CARDIO',
    'MOBILITY',
    'ENDURANCE',
    'HYPERTROPHY',
    'FAT_LOSS',
    'EXPLOSIVENESS',
    'SPEED'
);


ALTER TYPE public.goaltype OWNER TO jacked;

--
-- Name: hyrox_status; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.hyrox_status AS ENUM (
    'pending_review',
    'reviewed',
    'approved',
    'rejected'
);


ALTER TYPE public.hyrox_status OWNER TO jacked;

--
-- Name: hyrox_workout_goal; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.hyrox_workout_goal AS ENUM (
    'max_rounds_reps',
    'finish_quickly',
    'complete_rounds',
    'max_load',
    'pace_work',
    'endurance',
    'strength',
    'mixed',
    'unknown'
);


ALTER TYPE public.hyrox_workout_goal OWNER TO jacked;

--
-- Name: hyrox_workout_type; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.hyrox_workout_type AS ENUM (
    'amrap',
    'emom',
    'for_time',
    'rounds_for_time',
    'for_load',
    'buy_in',
    'cash_out',
    'time_cap',
    'ladder',
    'mini_circuit',
    'explicit_time_guidance',
    'unknown'
);


ALTER TYPE public.hyrox_workout_type OWNER TO jacked;

--
-- Name: metabolicdemand; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.metabolicdemand AS ENUM (
    'anabolic',
    'metabolic',
    'neural'
);


ALTER TYPE public.metabolicdemand OWNER TO jacked;

--
-- Name: metrictype; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.metrictype AS ENUM (
    'reps',
    'time',
    'time_under_tension',
    'distance',
    'calories'
);


ALTER TYPE public.metrictype OWNER TO jacked;

--
-- Name: movementrelationship; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.movementrelationship AS ENUM (
    'substitute',
    'progression',
    'regression',
    'variation',
    'superset',
    'contraindicated'
);


ALTER TYPE public.movementrelationship OWNER TO jacked;

--
-- Name: movementtier; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.movementtier AS ENUM (
    'diamond',
    'gold',
    'silver',
    'bronze'
);


ALTER TYPE public.movementtier OWNER TO jacked;

--
-- Name: movementtype; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.movementtype AS ENUM (
    'convention',
    'compound',
    'isolation',
    'plyometric',
    'mobility',
    'stretch',
    'isometric',
    'cardio',
    'conditioning',
    'olympic',
    'carry',
    'core',
    'rotation',
    'other'
);


ALTER TYPE public.movementtype OWNER TO jacked;

--
-- Name: muscleregion; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.muscleregion AS ENUM (
    'upper',
    'lower',
    'core',
    'full',
    'anterior lower',
    'posterior lower',
    'shoulder',
    'anterior upper',
    'posterior upper',
    'full body',
    'lower body',
    'upper body'
);


ALTER TYPE public.muscleregion OWNER TO jacked;

--
-- Name: musclerole; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.musclerole AS ENUM (
    'PRIMARY',
    'SECONDARY',
    'STABILIZER'
);


ALTER TYPE public.musclerole OWNER TO jacked;

--
-- Name: pattern; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.pattern AS ENUM (
    'push',
    'pull',
    'squat',
    'hinge',
    'lunge',
    'twist',
    'carry',
    'crawl',
    'jump',
    'throw',
    'grip',
    'core',
    'upper_push',
    'upper_pull',
    'lower_push',
    'lower_pull',
    'full_body',
    'cardio',
    'mobility',
    'other',
    'isolation',
    'horizontal_push',
    'horizontal_pull',
    'stretch',
    'conditioning',
    'plyometric',
    'vertical_pull',
    'olympic',
    'isometric',
    'vertical_push',
    'rotation'
);


ALTER TYPE public.pattern OWNER TO jacked;

--
-- Name: pattern_subtype; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.pattern_subtype AS ENUM (
    'squat',
    'hinge',
    'lunge',
    'horizontal_push',
    'horizontal_pull',
    'vertical_push',
    'vertical_pull',
    'rotation',
    'carry',
    'core',
    'plyometric',
    'isometric',
    'run',
    'row',
    'bike',
    'cycle',
    'swim',
    'elliptical',
    'sled_push',
    'sled_pull',
    'sled_drag',
    'burpee',
    'turkish_get_up',
    'farmer_carry',
    'waiter_carry',
    'suitcase_carry',
    'bear_crawl',
    'crab_walk',
    'mobility',
    'stretch',
    'activation',
    'dynamic_warmup',
    'static_stretch',
    'foam_roll',
    'conditioning',
    'anti_extension',
    'anti_rotation',
    'anti_lateral_flexion',
    'smr'
);


ALTER TYPE public.pattern_subtype OWNER TO jacked;

--
-- Name: patterntype_new; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.patterntype_new AS ENUM (
    'squat',
    'hinge',
    'lunge',
    'carry',
    'rotation',
    'core',
    'conditioning',
    'mobility',
    'horizontal_push',
    'horizontal_pull',
    'vertical_push',
    'vertical_pull'
);


ALTER TYPE public.patterntype_new OWNER TO jacked;

--
-- Name: personaaggression; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.personaaggression AS ENUM (
    'low',
    'moderate',
    'high',
    'extreme',
    'BALANCED',
    'MODERATE_AGGRESSIVE'
);


ALTER TYPE public.personaaggression OWNER TO jacked;

--
-- Name: personatone; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.personatone AS ENUM (
    'drill_sergeant',
    'supportive',
    'analytical',
    'motivational',
    'minimalist',
    'DRILL_SERGEANT',
    'SUPPORTIVE',
    'ANALYTICAL',
    'MOTIVATIONAL',
    'MINIMALIST'
);


ALTER TYPE public.personatone OWNER TO jacked;

--
-- Name: primarymuscle; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.primarymuscle AS ENUM (
    'quadriceps',
    'hamstrings',
    'glutes',
    'calves',
    'chest',
    'lats',
    'upper_back',
    'rear_delts',
    'front_delts',
    'side_delts',
    'biceps',
    'triceps',
    'forearms',
    'core',
    'obliques',
    'lower_back',
    'hip_flexors',
    'adductors',
    'abductors',
    'full_body'
);


ALTER TYPE public.primarymuscle OWNER TO jacked;

--
-- Name: primaryregion; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.primaryregion AS ENUM (
    'anterior lower',
    'posterior lower',
    'shoulder',
    'anterior upper',
    'posterior upper',
    'full body',
    'lower body',
    'upper body',
    'core'
);


ALTER TYPE public.primaryregion OWNER TO jacked;

--
-- Name: progressionstyle; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.progressionstyle AS ENUM (
    'SINGLE_PROGRESSION',
    'DOUBLE_PROGRESSION',
    'PAUSED_VARIATIONS',
    'BUILD_TO_DROP'
);


ALTER TYPE public.progressionstyle OWNER TO jacked;

--
-- Name: skilllevel; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.skilllevel AS ENUM (
    'beginner',
    'intermediate',
    'advanced',
    'expert'
);


ALTER TYPE public.skilllevel OWNER TO jacked;

--
-- Name: spinalcompression; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.spinalcompression AS ENUM (
    'none',
    'low',
    'moderate',
    'high'
);


ALTER TYPE public.spinalcompression OWNER TO jacked;

--
-- Name: splittemplate; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.splittemplate AS ENUM (
    'UPPER_LOWER',
    'PPL',
    'FULL_BODY',
    'HYBRID'
);


ALTER TYPE public.splittemplate OWNER TO jacked;

--
-- Name: training_modality_type; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.training_modality_type AS ENUM (
    'resistance',
    'cardio',
    'endurance',
    'explosive',
    'mobility',
    'stability'
);


ALTER TYPE public.training_modality_type OWNER TO jacked;

--
-- Name: visibility; Type: TYPE; Schema: public; Owner: jacked
--

CREATE TYPE public.visibility AS ENUM (
    'PRIVATE',
    'FRIENDS',
    'PUBLIC'
);


ALTER TYPE public.visibility OWNER TO jacked;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: activity_definitions; Type: TABLE; Schema: public; Owner: jacked
--

CREATE TABLE public.activity_definitions (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    category public.activitycategory NOT NULL,
    discipline_id integer,
    default_metric_type public.defaultmetrictype,
    default_equipment_tags json,
    created_at timestamp without time zone
);


ALTER TABLE public.activity_definitions OWNER TO jacked;

--
-- Name: activity_definitions_id_seq; Type: SEQUENCE; Schema: public; Owner: jacked
--

CREATE SEQUENCE public.activity_definitions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.activity_definitions_id_seq OWNER TO jacked;

--
-- Name: activity_definitions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jacked
--

ALTER SEQUENCE public.activity_definitions_id_seq OWNED BY public.activity_definitions.id;


--
-- Name: activity_muscle_map; Type: TABLE; Schema: public; Owner: jacked
--

CREATE TABLE public.activity_muscle_map (
    id integer NOT NULL,
    activity_definition_id integer NOT NULL,
    muscle_id integer NOT NULL,
    magnitude double precision NOT NULL,
    cns_impact double precision,
    created_at timestamp without time zone
);


ALTER TABLE public.activity_muscle_map OWNER TO jacked;

--
-- Name: activity_muscle_map_id_seq; Type: SEQUENCE; Schema: public; Owner: jacked
--

CREATE SEQUENCE public.activity_muscle_map_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.activity_muscle_map_id_seq OWNER TO jacked;

--
-- Name: activity_muscle_map_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jacked
--

ALTER SEQUENCE public.activity_muscle_map_id_seq OWNED BY public.activity_muscle_map.id;


--
-- Name: circuits_macro; Type: TABLE; Schema: public; Owner: jacked
--

CREATE TABLE public.circuits_macro (
    circuit_id integer NOT NULL,
    total_exercises integer NOT NULL,
    unique_movements integer NOT NULL,
    max_rx_weight_male double precision,
    max_rx_weight_female double precision,
    required_equipment jsonb NOT NULL,
    movement_pattern_counts jsonb NOT NULL,
    metabolic_profile jsonb NOT NULL,
    default_rounds integer,
    circuit_type_intensity double precision NOT NULL,
    data_completeness_score double precision NOT NULL,
    validation_errors jsonb NOT NULL,
    created_at double precision,
    updated_at double precision,
    primary_region public.primaryregion DEFAULT 'full body'::public.primaryregion NOT NULL
);


ALTER TABLE public.circuits_macro OWNER TO jacked;

--
-- Name: circuits_melted; Type: TABLE; Schema: public; Owner: jacked
--

CREATE TABLE public.circuits_melted (
    id integer NOT NULL,
    circuit_id integer NOT NULL,
    movement_id integer,
    exercise_sequence integer NOT NULL,
    movement_name character varying(200) NOT NULL,
    metric_type public.metrictype NOT NULL,
    reps integer,
    distance_meters double precision,
    duration_seconds integer,
    calories integer,
    rest_seconds integer,
    notes text,
    rx_weight_male double precision,
    rx_weight_female double precision,
    created_at double precision,
    updated_at double precision
);


ALTER TABLE public.circuits_melted OWNER TO jacked;

--
-- Name: circuits_melted_id_seq; Type: SEQUENCE; Schema: public; Owner: jacked
--

CREATE SEQUENCE public.circuits_melted_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.circuits_melted_id_seq OWNER TO jacked;

--
-- Name: circuits_melted_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jacked
--

ALTER SEQUENCE public.circuits_melted_id_seq OWNED BY public.circuits_melted.id;


--
-- Name: equipment; Type: TABLE; Schema: public; Owner: jacked
--

CREATE TABLE public.equipment (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.equipment OWNER TO jacked;

--
-- Name: equipment_backup_20260301; Type: TABLE; Schema: public; Owner: jacked
--

CREATE TABLE public.equipment_backup_20260301 (
    id integer,
    name character varying(100)
);


ALTER TABLE public.equipment_backup_20260301 OWNER TO jacked;

--
-- Name: equipment_id_seq; Type: SEQUENCE; Schema: public; Owner: jacked
--

CREATE SEQUENCE public.equipment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.equipment_id_seq OWNER TO jacked;

--
-- Name: equipment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jacked
--

ALTER SEQUENCE public.equipment_id_seq OWNED BY public.equipment.id;


--
-- Name: hyrox_scraping_log; Type: TABLE; Schema: public; Owner: jacked
--

CREATE TABLE public.hyrox_scraping_log (
    id integer NOT NULL,
    scrape_session_id character varying(255) NOT NULL,
    started_at timestamp with time zone,
    completed_at timestamp with time zone,
    total_workouts_found integer,
    workouts_scraped integer,
    workouts_saved integer,
    errors_count integer DEFAULT 0,
    has_errors boolean DEFAULT false,
    notes text,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.hyrox_scraping_log OWNER TO jacked;

--
-- Name: TABLE hyrox_scraping_log; Type: COMMENT; Schema: public; Owner: jacked
--

COMMENT ON TABLE public.hyrox_scraping_log IS 'Log of Hyrox scraping sessions';


--
-- Name: hyrox_scraping_log_id_seq; Type: SEQUENCE; Schema: public; Owner: jacked
--

CREATE SEQUENCE public.hyrox_scraping_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.hyrox_scraping_log_id_seq OWNER TO jacked;

--
-- Name: hyrox_scraping_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jacked
--

ALTER SEQUENCE public.hyrox_scraping_log_id_seq OWNED BY public.hyrox_scraping_log.id;


--
-- Name: hyrox_scraping_log_staging; Type: TABLE; Schema: public; Owner: jacked
--

CREATE TABLE public.hyrox_scraping_log_staging (
    id integer NOT NULL,
    scrape_session_id character varying(100) NOT NULL,
    started_at timestamp without time zone DEFAULT now(),
    completed_at timestamp without time zone,
    total_workouts_found integer DEFAULT 0,
    workouts_scraped integer DEFAULT 0,
    workouts_saved integer DEFAULT 0,
    errors_count integer DEFAULT 0,
    has_errors boolean DEFAULT false,
    error_summary text,
    user_agent text,
    notes text
);


ALTER TABLE public.hyrox_scraping_log_staging OWNER TO jacked;

--
-- Name: hyrox_scraping_log_staging_id_seq; Type: SEQUENCE; Schema: public; Owner: jacked
--

ALTER TABLE public.hyrox_scraping_log_staging ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.hyrox_scraping_log_staging_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: hyrox_workout_lines; Type: TABLE; Schema: public; Owner: jacked
--

CREATE TABLE public.hyrox_workout_lines (
    id integer NOT NULL,
    workout_id integer NOT NULL,
    line_text text NOT NULL,
    line_number integer DEFAULT 0,
    is_rest boolean DEFAULT false,
    movement_name character varying(500),
    reps integer,
    distance_meters integer,
    duration_seconds integer,
    weight_text character varying(50),
    calories integer,
    movement_id integer,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.hyrox_workout_lines OWNER TO jacked;

--
-- Name: TABLE hyrox_workout_lines; Type: COMMENT; Schema: public; Owner: jacked
--

COMMENT ON TABLE public.hyrox_workout_lines IS 'Individual movement lines within Hyrox workouts';


--
-- Name: hyrox_workout_lines_id_seq; Type: SEQUENCE; Schema: public; Owner: jacked
--

CREATE SEQUENCE public.hyrox_workout_lines_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.hyrox_workout_lines_id_seq OWNER TO jacked;

--
-- Name: hyrox_workout_lines_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jacked
--

ALTER SEQUENCE public.hyrox_workout_lines_id_seq OWNED BY public.hyrox_workout_lines.id;


--
-- Name: hyrox_workout_movements_staging; Type: TABLE; Schema: public; Owner: jacked
--

CREATE TABLE public.hyrox_workout_movements_staging (
    id integer NOT NULL,
    workout_id integer NOT NULL,
    line_id integer,
    movement_name character varying(200) NOT NULL,
    movement_type character varying(50),
    reps integer,
    distance_meters double precision,
    duration_seconds integer,
    calories integer,
    weight_male double precision,
    weight_female double precision,
    is_max_effort boolean DEFAULT false,
    notes text,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.hyrox_workout_movements_staging OWNER TO jacked;

--
-- Name: hyrox_workout_movements_staging_id_seq; Type: SEQUENCE; Schema: public; Owner: jacked
--

ALTER TABLE public.hyrox_workout_movements_staging ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.hyrox_workout_movements_staging_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: hyrox_workout_tags; Type: TABLE; Schema: public; Owner: jacked
--

CREATE TABLE public.hyrox_workout_tags (
    id integer NOT NULL,
    workout_id integer NOT NULL,
    tag_name character varying(100) NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.hyrox_workout_tags OWNER TO jacked;

--
-- Name: TABLE hyrox_workout_tags; Type: COMMENT; Schema: public; Owner: jacked
--

COMMENT ON TABLE public.hyrox_workout_tags IS 'Tags associated with Hyrox workouts';


--
-- Name: hyrox_workout_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: jacked
--

CREATE SEQUENCE public.hyrox_workout_tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.hyrox_workout_tags_id_seq OWNER TO jacked;

--
-- Name: hyrox_workout_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jacked
--

ALTER SEQUENCE public.hyrox_workout_tags_id_seq OWNED BY public.hyrox_workout_tags.id;


--
-- Name: hyrox_workouts; Type: TABLE; Schema: public; Owner: jacked
--

CREATE TABLE public.hyrox_workouts (
    id integer NOT NULL,
    wod_id character varying(255) NOT NULL,
    name character varying(500) NOT NULL,
    url text,
    badge character varying(100),
    workout_type character varying(50),
    workout_goal character varying(50),
    time_specification character varying(100),
    total_time_minutes integer,
    time_cap_minutes integer,
    has_buy_in boolean DEFAULT false,
    has_cash_out boolean DEFAULT false,
    is_complex boolean DEFAULT false,
    background_image text,
    favorites_count integer DEFAULT 0,
    comments_count integer DEFAULT 0,
    full_description text,
    source_page character varying(100) DEFAULT 'hyrox_workouts'::character varying,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.hyrox_workouts OWNER TO jacked;

--
-- Name: TABLE hyrox_workouts; Type: COMMENT; Schema: public; Owner: jacked
--

COMMENT ON TABLE public.hyrox_workouts IS 'Hyrox workout definitions from wodwell.com';


--
-- Name: hyrox_workouts_id_seq; Type: SEQUENCE; Schema: public; Owner: jacked
--

CREATE SEQUENCE public.hyrox_workouts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.hyrox_workouts_id_seq OWNER TO jacked;

--
-- Name: hyrox_workouts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jacked
--

ALTER SEQUENCE public.hyrox_workouts_id_seq OWNED BY public.hyrox_workouts.id;


--
-- Name: migration_version; Type: TABLE; Schema: public; Owner: jacked
--

CREATE TABLE public.migration_version (
    version character varying(50) NOT NULL,
    description text,
    applied_at timestamp without time zone DEFAULT now(),
    checksum character varying(64)
);


ALTER TABLE public.migration_version OWNER TO jacked;

--
-- Name: movement_coaching_cues; Type: TABLE; Schema: public; Owner: jacked
--

CREATE TABLE public.movement_coaching_cues (
    id integer NOT NULL,
    movement_id integer NOT NULL,
    cue_text text NOT NULL,
    "order" integer
);


ALTER TABLE public.movement_coaching_cues OWNER TO jacked;

--
-- Name: movement_coaching_cues_id_seq; Type: SEQUENCE; Schema: public; Owner: jacked
--

CREATE SEQUENCE public.movement_coaching_cues_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.movement_coaching_cues_id_seq OWNER TO jacked;

--
-- Name: movement_coaching_cues_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jacked
--

ALTER SEQUENCE public.movement_coaching_cues_id_seq OWNED BY public.movement_coaching_cues.id;


--
-- Name: movement_equipment; Type: TABLE; Schema: public; Owner: jacked
--

CREATE TABLE public.movement_equipment (
    movement_id integer NOT NULL,
    equipment_id integer NOT NULL
);


ALTER TABLE public.movement_equipment OWNER TO jacked;

--
-- Name: movement_equipment_backup_20260301; Type: TABLE; Schema: public; Owner: jacked
--

CREATE TABLE public.movement_equipment_backup_20260301 (
    movement_id integer,
    equipment_id integer
);


ALTER TABLE public.movement_equipment_backup_20260301 OWNER TO jacked;

--
-- Name: movement_muscle_map; Type: TABLE; Schema: public; Owner: jacked
--

CREATE TABLE public.movement_muscle_map (
    id integer NOT NULL,
    movement_id integer NOT NULL,
    muscle_id integer NOT NULL,
    role public.musclerole NOT NULL,
    magnitude double precision NOT NULL
);


ALTER TABLE public.movement_muscle_map OWNER TO jacked;

--
-- Name: movement_muscle_map_backup_20260301; Type: TABLE; Schema: public; Owner: jacked
--

CREATE TABLE public.movement_muscle_map_backup_20260301 (
    id integer,
    movement_id integer,
    muscle_id integer,
    role public.musclerole,
    magnitude double precision
);


ALTER TABLE public.movement_muscle_map_backup_20260301 OWNER TO jacked;

--
-- Name: movement_muscle_map_id_seq; Type: SEQUENCE; Schema: public; Owner: jacked
--

CREATE SEQUENCE public.movement_muscle_map_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.movement_muscle_map_id_seq OWNER TO jacked;

--
-- Name: movement_muscle_map_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jacked
--

ALTER SEQUENCE public.movement_muscle_map_id_seq OWNED BY public.movement_muscle_map.id;


--
-- Name: movements; Type: TABLE; Schema: public; Owner: jacked
--

CREATE TABLE public.movements (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    primary_muscle public.primarymuscle NOT NULL,
    primary_region public.primaryregion NOT NULL,
    compound boolean,
    is_complex_lift boolean,
    is_unilateral boolean,
    metric_type public.metrictype NOT NULL,
    spinal_compression public.spinalcompression DEFAULT 'none'::public.spinalcompression NOT NULL,
    bodyweight_possible boolean DEFAULT false,
    dumbbell_possible boolean DEFAULT false,
    kettlebell_possible boolean DEFAULT false,
    barbell_possible boolean DEFAULT false,
    machine_possible boolean DEFAULT false,
    band_possible boolean DEFAULT false,
    plate_or_med_ball_possible boolean DEFAULT false,
    regression_to_move integer,
    progression_to_move integer,
    variation_to_move integer,
    discipline public.disciplinetype_new3,
    pattern public.patterntype_new,
    pattern_subtype public.pattern_subtype
);


ALTER TABLE public.movements OWNER TO jacked;

--
-- Name: movements_backup_20260228; Type: TABLE; Schema: public; Owner: jacked
--

CREATE TABLE public.movements_backup_20260228 (
    id integer NOT NULL,
    name character varying(255),
    primary_region public.primaryregion,
    bodyweight_possible boolean,
    dumbbell_possible boolean,
    kettlebell_possible boolean,
    barbell_possible boolean,
    machine_possible boolean,
    band_possible boolean,
    plate_or_med_ball_possible boolean,
    pattern public.patterntype_new,
    pattern_subtype public.pattern_subtype,
    backup_timestamp timestamp with time zone
);


ALTER TABLE public.movements_backup_20260228 OWNER TO jacked;

--
-- Name: TABLE movements_backup_20260228; Type: COMMENT; Schema: public; Owner: jacked
--

COMMENT ON TABLE public.movements_backup_20260228 IS 'Backup of movements table before manual updates on 2026-02-28. Contains 11 target columns for rollback capability.';


--
-- Name: movements_id_seq; Type: SEQUENCE; Schema: public; Owner: jacked
--

CREATE SEQUENCE public.movements_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.movements_id_seq OWNER TO jacked;

--
-- Name: movements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jacked
--

ALTER SEQUENCE public.movements_id_seq OWNED BY public.movements.id;


--
-- Name: muscles; Type: TABLE; Schema: public; Owner: jacked
--

CREATE TABLE public.muscles (
    id integer NOT NULL,
    slug character varying(100) NOT NULL,
    region public.muscleregion
);


ALTER TABLE public.muscles OWNER TO jacked;

--
-- Name: muscles_id_seq; Type: SEQUENCE; Schema: public; Owner: jacked
--

CREATE SEQUENCE public.muscles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.muscles_id_seq OWNER TO jacked;

--
-- Name: muscles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jacked
--

ALTER SEQUENCE public.muscles_id_seq OWNED BY public.muscles.id;


--
-- Name: programs_backup_20260226; Type: TABLE; Schema: public; Owner: jacked
--

CREATE TABLE public.programs_backup_20260226 (
    id integer,
    user_id integer,
    start_date date,
    duration_weeks integer,
    goal_1 public.goaltype,
    goal_2 public.goaltype,
    goal_3 public.goaltype,
    goal_weight_1 integer,
    goal_weight_2 integer,
    goal_weight_3 integer,
    split_template public.splittemplate,
    days_per_week integer,
    progression_style public.progressionstyle,
    hybrid_definition json,
    deload_every_n_microcycles integer,
    is_active boolean,
    created_at timestamp without time zone,
    is_template boolean,
    visibility public.visibility,
    name character varying(100),
    macro_cycle_id integer,
    max_session_duration integer,
    persona_aggression public.personaaggression,
    persona_tone public.personatone,
    generation_in_progress boolean
);


ALTER TABLE public.programs_backup_20260226 OWNER TO jacked;

--
-- Name: tags; Type: TABLE; Schema: public; Owner: jacked
--

CREATE TABLE public.tags (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.tags OWNER TO jacked;

--
-- Name: tags_id_seq; Type: SEQUENCE; Schema: public; Owner: jacked
--

CREATE SEQUENCE public.tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tags_id_seq OWNER TO jacked;

--
-- Name: tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jacked
--

ALTER SEQUENCE public.tags_id_seq OWNED BY public.tags.id;


--
-- Name: activity_definitions id; Type: DEFAULT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.activity_definitions ALTER COLUMN id SET DEFAULT nextval('public.activity_definitions_id_seq'::regclass);


--
-- Name: activity_muscle_map id; Type: DEFAULT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.activity_muscle_map ALTER COLUMN id SET DEFAULT nextval('public.activity_muscle_map_id_seq'::regclass);


--
-- Name: circuits_melted id; Type: DEFAULT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.circuits_melted ALTER COLUMN id SET DEFAULT nextval('public.circuits_melted_id_seq'::regclass);


--
-- Name: equipment id; Type: DEFAULT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.equipment ALTER COLUMN id SET DEFAULT nextval('public.equipment_id_seq'::regclass);


--
-- Name: hyrox_scraping_log id; Type: DEFAULT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.hyrox_scraping_log ALTER COLUMN id SET DEFAULT nextval('public.hyrox_scraping_log_id_seq'::regclass);


--
-- Name: hyrox_workout_lines id; Type: DEFAULT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.hyrox_workout_lines ALTER COLUMN id SET DEFAULT nextval('public.hyrox_workout_lines_id_seq'::regclass);


--
-- Name: hyrox_workout_tags id; Type: DEFAULT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.hyrox_workout_tags ALTER COLUMN id SET DEFAULT nextval('public.hyrox_workout_tags_id_seq'::regclass);


--
-- Name: hyrox_workouts id; Type: DEFAULT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.hyrox_workouts ALTER COLUMN id SET DEFAULT nextval('public.hyrox_workouts_id_seq'::regclass);


--
-- Name: movement_coaching_cues id; Type: DEFAULT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.movement_coaching_cues ALTER COLUMN id SET DEFAULT nextval('public.movement_coaching_cues_id_seq'::regclass);


--
-- Name: movement_muscle_map id; Type: DEFAULT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.movement_muscle_map ALTER COLUMN id SET DEFAULT nextval('public.movement_muscle_map_id_seq'::regclass);


--
-- Name: movements id; Type: DEFAULT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.movements ALTER COLUMN id SET DEFAULT nextval('public.movements_id_seq'::regclass);


--
-- Name: muscles id; Type: DEFAULT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.muscles ALTER COLUMN id SET DEFAULT nextval('public.muscles_id_seq'::regclass);


--
-- Name: tags id; Type: DEFAULT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.tags ALTER COLUMN id SET DEFAULT nextval('public.tags_id_seq'::regclass);


--
-- Data for Name: activity_definitions; Type: TABLE DATA; Schema: public; Owner: jacked
--

COPY public.activity_definitions (id, name, category, discipline_id, default_metric_type, default_equipment_tags, created_at) FROM stdin;
1	City Run	CARDIO	\N	DISTANCE	[]	2026-01-19 23:26:38.956151
2	Trail Run	CARDIO	\N	DISTANCE	[]	2026-01-19 23:26:38.960022
5	Rucking	CARDIO	\N	DISTANCE	["backpack"]	2026-01-19 23:26:38.96403
6	Tennis	SPORT	\N	TIME	["racket"]	2026-01-19 23:26:38.965377
7	Padel	SPORT	\N	TIME	["racket"]	2026-01-19 23:26:38.966711
8	Pickleball	SPORT	\N	TIME	["racket"]	2026-01-19 23:26:38.968043
9	Squash	SPORT	\N	TIME	["racket"]	2026-01-19 23:26:38.969264
10	Badminton	SPORT	\N	TIME	["racket"]	2026-01-19 23:26:38.970522
11	Golf	SPORT	\N	TIME	["clubs"]	2026-01-19 23:26:38.971758
12	Bouldering	SPORT	\N	TIME	[]	2026-01-19 23:26:38.97306
13	Basketball	SPORT	\N	TIME	["ball"]	2026-01-19 23:26:38.97433
14	Indoor Football (6-a-side)	SPORT	\N	TIME	[]	2026-01-19 23:26:38.975596
15	Football (11-a-side)	SPORT	\N	TIME	[]	2026-01-19 23:26:38.976864
16	Surfing	SPORT	\N	TIME	["board"]	2026-01-19 23:26:38.978121
17	Kayaking	SPORT	\N	TIME	["kayak"]	2026-01-19 23:26:38.979347
18	Pilates	MOBILITY	\N	TIME	[]	2026-01-19 23:26:38.980573
19	Yoga	MOBILITY	\N	TIME	["mat"]	2026-01-19 23:26:38.981798
3	Cycling	CARDIO	\N	DISTANCE	["bike"]	2026-01-19 23:26:38.96142
4	Swimming	CARDIO	\N	DISTANCE	[]	2026-01-19 23:26:38.96279
\.


--
-- Data for Name: activity_muscle_map; Type: TABLE DATA; Schema: public; Owner: jacked
--

COPY public.activity_muscle_map (id, activity_definition_id, muscle_id, magnitude, cns_impact, created_at) FROM stdin;
\.


--
-- Data for Name: circuits_macro; Type: TABLE DATA; Schema: public; Owner: jacked
--

COPY public.circuits_macro (circuit_id, total_exercises, unique_movements, max_rx_weight_male, max_rx_weight_female, required_equipment, movement_pattern_counts, metabolic_profile, default_rounds, circuit_type_intensity, data_completeness_score, validation_errors, created_at, updated_at, primary_region) FROM stdin;
148	12	6	\N	\N	[]	{"core": 1, "squat": 2, "plyometric": 1, "conditioning": 2}	{"neural": 0.0, "anabolic": 0.2, "metabolic": 0.8}	12	1.1	1	[]	1769674698.814955	1769676299.821618	full body
109	3	1	50	35	[]	{"squat": 1}	{"neural": 0.0, "anabolic": 0.35, "metabolic": 0.65}	\N	1.15	1	[]	1769674698.826794	1769676299.824076	lower body
110	4	1	\N	\N	[225, 238]	{"lunge": 1}	{"neural": 0.0, "anabolic": 0.5, "metabolic": 0.5}	2	0.95	1	[]	1769674698.831073	1769676299.825231	full body
112	4	1	\N	\N	[225, 238]	{"lunge": 1}	{"neural": 0.0, "anabolic": 0.30000000000000004, "metabolic": 0.7000000000000001}	2	1.1	1	[]	1769674698.834511	1769676299.827053	full body
114	1	1	135	95	[]	{"hinge": 1}	{"neural": 0.0, "anabolic": 0.30000000000000004, "metabolic": 0.7000000000000001}	\N	1.1	1	[]	1769674698.837889	1769676299.828116	posterior lower
119	15	3	50	35	[]	{"hinge": 5, "horizontal_pull": 10}	{"neural": 0.1, "anabolic": 0.3, "metabolic": 0.6}	5	1.05	1	[]	1769674698.866812	1769676299.833045	upper body
129	12	2	70	53	[]	{"squat": 3, "conditioning": 3}	{"neural": 0.1, "anabolic": 0.3, "metabolic": 0.6}	\N	1.05	1	[]	1769674698.881054	1769676299.835321	full body
146	12	6	\N	\N	[]	{"core": 1, "squat": 2, "plyometric": 1, "conditioning": 2}	{"neural": 0.0, "anabolic": 0.2, "metabolic": 0.8}	12	1.1	1	[]	1769674698.896175	1769676299.837824	full body
150	1	0	135	95	[]	{}	{"neural": 0.0, "anabolic": 0.30000000000000004, "metabolic": 0.7000000000000001}	\N	1.1	1	[]	1769674698.89797	1769676299.838478	full body
157	2	2	\N	\N	[217]	{"cardio": 1, "vertical_pull": 1}	{"neural": 0.0, "anabolic": 0.25, "metabolic": 0.75}	\N	1.15	1	[]	1769674698.903962	1769676299.839698	full body
134	5	2	\N	\N	[211, 225]	{"lunge": 1, "squat": 2}	{"neural": 0.0, "anabolic": 0.30000000000000004, "metabolic": 0.7000000000000001}	\N	1.1	1	[]	1769675466.13923	1769676299.841246	lower body
122	2	2	\N	\N	[]	{"squat": 1, "cardio": 1}	{"neural": 0.0, "anabolic": 0.2, "metabolic": 0.8}	3	1.1	1	[]	1769675466.14727	1769676299.842503	posterior lower
152	1	1	\N	\N	[]	{"cardio": 1}	{"neural": 0.0, "anabolic": 0.2, "metabolic": 0.8}	3	1.1	1	[]	1769675466.15074	1769676299.843461	posterior lower
136	5	2	\N	\N	[211, 225]	{"lunge": 1, "squat": 2}	{"neural": 0.0, "anabolic": 0.30000000000000004, "metabolic": 0.7000000000000001}	\N	1.1	1	[]	1769675466.160787	1769676299.844964	lower body
153	3	2	95	65	[]	{"squat": 1, "vertical_push": 1}	{"neural": 0.0, "anabolic": 0.30000000000000004, "metabolic": 0.7000000000000001}	5	1.1	1	[]	1769675466.166934	1769676299.846225	lower body
116	7	3	50	35	[228]	{"cardio": 4, "horizontal_push": 2}	{"neural": 0.1, "anabolic": 0.3, "metabolic": 0.6}	\N	1.05	1	[]	1769675466.178925	1769676299.848648	posterior lower
107	2	2	\N	\N	[243]	{"carry": 1, "cardio": 1}	{"neural": 0.0, "anabolic": 0.2, "metabolic": 0.8}	10	1.1	1	[]	1769675466.184525	1769676299.849933	full body
121	4	2	\N	\N	[217]	{"core": 1, "vertical_push": 2}	{"neural": 0.0, "anabolic": 0.42857142857142855, "metabolic": 0.5714285714285714}	3	0.95	1	[]	1769675466.191283	1769676299.851446	upper body
124	2	2	\N	\N	[]	{"squat": 1, "cardio": 1}	{"neural": 0.0, "anabolic": 0.2, "metabolic": 0.8}	3	1.1	1	[]	1769675466.19654	1769676299.852643	posterior lower
126	9	2	\N	\N	[]	{"core": 3, "conditioning": 3}	{"neural": 0.0, "anabolic": 0.2, "metabolic": 0.8}	\N	1.1	1	[]	1769675466.208324	1769676299.855081	full body
133	4	2	\N	\N	[]	{"conditioning": 1, "vertical_push": 1}	{"neural": 0.0, "anabolic": 0.42857142857142855, "metabolic": 0.5714285714285714}	\N	0.95	1	[]	1769675466.213313	1769676299.856303	upper body
140	3	3	50	35	[213]	{"core": 1, "isolation": 1, "conditioning": 1}	{"neural": 0.0, "anabolic": 0.2, "metabolic": 0.8}	3	1.1	1	[]	1769675466.219867	1769676299.857778	full body
141	9	2	315	225	[]	{"hinge": 3, "plyometric": 3}	{"neural": 0.0, "anabolic": 0.30000000000000004, "metabolic": 0.7000000000000001}	\N	1.1	1	[]	1769675466.232074	1769676299.860067	posterior lower
145	5	0	20	14	[]	{}	{"neural": 0.0, "anabolic": 0.35, "metabolic": 0.65}	\N	1.15	1	[]	1769675466.233194	1769676299.860641	full body
143	9	2	315	225	[]	{"hinge": 3, "plyometric": 3}	{"neural": 0.1, "anabolic": 0.4, "metabolic": 0.5}	\N	1.05	1	[]	1769675466.245475	1769676299.862818	posterior lower
155	3	2	95	65	[]	{"squat": 1, "vertical_push": 1}	{"neural": 0.0, "anabolic": 0.30000000000000004, "metabolic": 0.7000000000000001}	5	1.1	1	[]	1769675466.250267	1769676299.864213	lower body
\.


--
-- Data for Name: circuits_melted; Type: TABLE DATA; Schema: public; Owner: jacked
--

COPY public.circuits_melted (id, circuit_id, movement_id, exercise_sequence, movement_name, metric_type, reps, distance_meters, duration_seconds, calories, rest_seconds, notes, rx_weight_male, rx_weight_female, created_at, updated_at) FROM stdin;
121	134	500	1	Squat Cleans	reps	20	\N	\N	\N	\N	\N	\N	\N	1769644915.285291	1769644914.827537
161	110	400	1	Row	calories	\N	\N	\N	20	\N	Calories: M 20 / F 25	\N	\N	1769644915.337755	1770048025.891026
123	134	6	3	Walking Lunge	reps	20	\N	\N	\N	\N	\N	\N	\N	1769644915.289077	1769644914.827537
163	110	400	3	Row	calories	\N	\N	\N	20	\N	Calories: M 20 / F 25	\N	\N	1769644915.339866	1770048025.891026
125	134	500	5	Squat Cleans	reps	20	\N	\N	\N	\N	\N	\N	\N	1769644915.292959	1769644914.827537
126	122	389	1	Run	distance	\N	800	\N	\N	\N	\N	\N	\N	1769644915.297555	1769644914.827537
127	122	376	2	Air Squats	reps	80	\N	\N	\N	\N	\N	\N	\N	1769644915.299651	1769644914.827537
128	148	395	1	Wall Walk	reps	1	\N	\N	\N	\N	\N	\N	\N	1769644915.30139	1769644914.827537
129	148	381	2	Candlestick Rocks	reps	2	\N	\N	\N	\N	\N	\N	\N	1769644915.302576	1769644914.827537
130	148	379	3	Burpees	reps	3	\N	\N	\N	\N	\N	\N	\N	1769644915.303637	1769644914.827537
165	112	400	1	Row	calories	\N	\N	\N	20	\N	Calories: M 20 / F 25	\N	\N	1769644915.341824	1770048025.891026
167	112	400	3	Row	calories	\N	\N	\N	20	\N	Calories: M 20 / F 25	\N	\N	1769644915.343053	1770048025.891026
133	148	376	6	Air Squats	reps	6	\N	\N	\N	\N	\N	\N	\N	1769644915.307255	1769644914.827537
135	148	388	8	Jumping Squats	reps	8	\N	\N	\N	\N	\N	\N	\N	1769644915.309496	1769644914.827537
140	152	389	1	Run	distance	\N	1600	\N	\N	\N	\N	\N	\N	1769644915.314283	1769644914.827537
141	136	500	1	Squat Cleans	reps	20	\N	\N	\N	\N	\N	\N	\N	1769644915.315758	1769644914.827537
143	136	6	3	Walking Lunge	reps	20	\N	\N	\N	\N	\N	\N	\N	1769644915.317658	1769644914.827537
145	136	500	5	Squat Cleans	reps	20	\N	\N	\N	\N	\N	\N	\N	1769644915.319568	1769644914.827537
146	153	393	1	Thrusters	reps	10	\N	\N	\N	\N	\N	\N	\N	1769644915.321273	1769644914.827537
148	153	390	3	Handstand Hold	time	\N	\N	30	\N	\N	(♀ 65 lb) (♂ 95 lb)	95	65	1769644915.323396	1769644914.827537
149	116	389	1	Run	distance	\N	400	\N	\N	\N	\N	\N	\N	1769644915.324846	1769644914.827537
151	116	389	3	Run	distance	\N	400	\N	\N	\N	\N	\N	\N	1769644915.326623	1769644914.827537
152	116	411	4	ring push ups	reps	50	\N	\N	\N	\N	\N	\N	\N	1769644915.32763	1769644914.827537
153	116	389	5	Run	distance	\N	400	\N	\N	\N	\N	\N	\N	1769644915.328667	1769644914.827537
154	116	404	6	hand release push ups	reps	50	\N	\N	\N	\N	\N	\N	\N	1769644915.329715	1769644914.827537
155	116	389	7	Run	distance	\N	400	\N	\N	\N	\N	\N	\N	1769644915.33076	1769644914.827537
156	107	412	1	Sandbag Carry	distance	\N	18	\N	\N	\N	\N	\N	\N	1769644915.332498	1769644914.827537
158	109	385	1	Dumbbell Thrusters	reps	4	\N	\N	\N	\N	(♀ 35-lb dumbbells) (♂ 50-lb dumbbells)	50	35	1769644915.334939	1769644914.827537
164	110	401	4	Box Step-Ups	reps	90	\N	\N	\N	\N	\N	\N	\N	1769644915.340843	1769644914.827537
168	112	401	4	Box Step-Ups	reps	90	\N	\N	\N	\N	\N	\N	\N	1769644915.343831	1769644914.827537
171	119	374	2	Lateral Burpees Over The Rower	reps	30	\N	\N	\N	\N	\N	\N	\N	1769644915.347503	1769644914.827537
172	119	435	3	Alternating Dumbbell Snatches	reps	30	\N	\N	\N	\N	(♀ 35-lb dumbbell) (♂ 50-lb dumbbell)	50	35	1769644915.348375	1769644914.827537
174	119	374	5	Lateral Burpees Over The Rower	reps	24	\N	\N	\N	\N	\N	\N	\N	1769644915.349956	1769644914.827537
175	119	435	6	Alternating Dumbbell Snatches	reps	24	\N	\N	\N	\N	(♀ 35-lb dumbbell) (♂ 50-lb dumbbell)	50	35	1769644915.350761	1769644914.827537
177	119	374	8	Lateral Burpees Over The Rower	reps	18	\N	\N	\N	\N	\N	\N	\N	1769644915.352232	1769644914.827537
178	119	435	9	Alternating Dumbbell Snatches	reps	18	\N	\N	\N	\N	(♀ 35-lb dumbbell) (♂ 50-lb dumbbell)	50	35	1769644915.353065	1769644914.827537
180	119	374	11	Lateral Burpees Over The Rower	reps	12	\N	\N	\N	\N	\N	\N	\N	1769644915.354737	1769644914.827537
181	119	435	12	Alternating Dumbbell Snatches	reps	12	\N	\N	\N	\N	(♀ 35-lb dumbbell) (♂ 50-lb dumbbell)	50	35	1769644915.355529	1769644914.827537
183	119	374	14	Lateral Burpees Over The Rower	reps	6	\N	\N	\N	\N	\N	\N	\N	1769644915.357327	1769644914.827537
184	119	435	15	Alternating Dumbbell Snatches	reps	6	\N	\N	\N	\N	(♀ 35-lb dumbbell) (♂ 50-lb dumbbell)	50	35	1769644915.358173	1769644914.827537
185	121	488	1	Handstand Walk	distance	\N	15	\N	\N	\N	\N	\N	\N	1769644915.359514	1769644914.827537
186	121	407	2	knees to elbows	reps	999	\N	\N	\N	\N	max	\N	\N	1769644915.360466	1769644914.827537
187	121	488	3	Handstand Walk	distance	\N	15	\N	\N	\N	\N	\N	\N	1769644915.361361	1769644914.827537
189	124	389	1	Run	distance	\N	800	\N	\N	\N	\N	\N	\N	1769644915.363323	1769644914.827537
190	124	376	2	Air Squats	reps	80	\N	\N	\N	\N	\N	\N	\N	1769644915.3642	1769644914.827537
200	129	454	1	Russian Kettlebell Swings	reps	30	\N	\N	\N	\N	\N	\N	\N	1769644915.372787	1769644914.827537
160	109	383	3	double unders	reps	24	\N	\N	\N	\N	\N	\N	\N	1769644915.336541	1770047268.14542
162	110	391	2	Single Leg Squats	reps	30	\N	\N	\N	\N	\N	\N	\N	1769644915.338788	1770047268.14542
166	112	391	2	Single Leg Squats	reps	30	\N	\N	\N	\N	\N	\N	\N	1769644915.342446	1770047268.14542
188	121	6	4	Walking Lunges	reps	999	\N	\N	\N	\N	max	\N	\N	1769644915.3621	1770047268.14542
192	126	43	2	Box Jumps	reps	30	\N	\N	\N	\N	\N	\N	\N	1769644915.366199	1770047268.14542
159	109	394	2	toes to bars	reps	6	\N	\N	\N	\N	\N	\N	\N	1769644915.335745	1769644914.827537
150	116	15	2	Dumbbell Bench Presses	reps	50	\N	\N	\N	\N	(♀ 35-lb dumbbells) (♂ 50-lb dumbbells)	50	35	1769644915.32565	1769644914.827537
169	114	33	1	Clean And Jerks	reps	30	\N	\N	\N	\N	(♀ 95-lb barbell) (♂ 135-lb barbell)	135	95	1769644915.34511	1769644914.827537
191	126	37	1	Plank Hold	time	\N	\N	120	\N	\N	\N	\N	\N	1769644915.365485	1769644914.827537
194	126	37	4	Plank Hold	time	\N	\N	120	\N	\N	\N	\N	\N	1769644915.367805	1769644914.827537
197	126	37	7	Plank Hold	time	\N	\N	120	\N	\N	\N	\N	\N	1769644915.370158	1769644914.827537
201	129	491	2	Kettlebell Goblet Squats	reps	30	\N	\N	\N	\N	\N	\N	\N	1769644915.373609	1769644914.827537
228	145	400	1	Row	calories	\N	\N	\N	20	\N	Calories: M 20	\N	\N	1769644915.400334	1770048025.891026
204	129	454	5	Russian Kettlebell Swings	reps	20	\N	\N	\N	\N	\N	\N	\N	1769644915.37585	1769644914.827537
205	129	491	6	Kettlebell Goblet Squats	reps	20	\N	\N	\N	\N	\N	\N	\N	1769644915.376664	1769644914.827537
208	129	454	9	Russian Kettlebell Swings	reps	10	\N	\N	\N	\N	\N	\N	\N	1769644915.379664	1769644914.827537
209	129	491	10	Kettlebell Goblet Squats	reps	10	\N	\N	\N	\N	\N	\N	\N	1769644915.380708	1769644914.827537
213	133	501	2	Strict Handstand Push Ups	reps	999	\N	\N	\N	\N	max	\N	\N	1769644915.384878	1769644914.827537
215	133	502	4	Strict Ring Dips	reps	999	\N	\N	\N	\N	max	\N	\N	1769644915.386764	1769644914.827537
216	140	261	1	Rope Climb	reps	4	\N	\N	\N	\N	Height: 15 ft	\N	\N	1769644915.388494	1769644914.827537
217	140	398	2	GHD sit ups	reps	40	\N	\N	\N	\N	\N	\N	\N	1769644915.389668	1769644914.827537
219	141	382	1	Deadlifts	reps	21	\N	\N	\N	\N	\N	\N	\N	1769644915.391896	1769644914.827537
221	141	379	3	Burpees	time	\N	\N	120	\N	\N	\N	\N	\N	1769644915.393557	1769644914.827537
222	141	382	4	Deadlifts	reps	15	\N	\N	\N	\N	\N	\N	\N	1769644915.394449	1769644914.827537
224	141	379	6	Burpees	time	\N	\N	120	\N	\N	\N	\N	\N	1769644915.396226	1769644914.827537
225	141	382	7	Deadlifts	reps	9	\N	\N	\N	\N	\N	\N	\N	1769644915.397227	1769644914.827537
134	148	131	7	Sit-Ups	reps	7	\N	\N	\N	\N	\N	\N	\N	1769644915.308405	1769644914.827537
227	141	379	9	Burpees	time	\N	\N	120	\N	\N	(♀ 225 lb) (♂ 315 lb)	315	225	1769644915.398974	1769644914.827537
233	146	395	1	Wall Walk	reps	1	\N	\N	\N	\N	\N	\N	\N	1769644915.405973	1769644914.827537
234	146	381	2	Candlestick Rocks	reps	2	\N	\N	\N	\N	\N	\N	\N	1769644915.407016	1769644914.827537
235	146	379	3	Burpees	reps	3	\N	\N	\N	\N	\N	\N	\N	1769644915.407915	1769644914.827537
238	146	376	6	Air Squats	reps	6	\N	\N	\N	\N	\N	\N	\N	1769644915.410074	1769644914.827537
240	146	388	8	Jumping Squats	reps	8	\N	\N	\N	\N	\N	\N	\N	1769644915.411604	1769644914.827537
245	143	382	1	Deadlifts	reps	21	\N	\N	\N	\N	\N	\N	\N	1769644915.415436	1769644914.827537
247	143	379	3	Burpees	time	\N	\N	120	\N	\N	\N	\N	\N	1769644915.41691	1769644914.827537
248	143	382	4	Deadlifts	reps	15	\N	\N	\N	\N	\N	\N	\N	1769644915.417707	1769644914.827537
250	143	379	6	Burpees	time	\N	\N	120	\N	\N	\N	\N	\N	1769644915.419164	1769644914.827537
251	143	382	7	Deadlifts	reps	9	\N	\N	\N	\N	\N	\N	\N	1769644915.419999	1769644914.827537
253	143	379	9	Burpees	time	\N	\N	120	\N	\N	(♀ 225 lb) (♂ 315 lb)	315	225	1769644915.421477	1769644914.827537
255	155	393	1	Thrusters	reps	10	\N	\N	\N	\N	\N	\N	\N	1769644915.423651	1769644914.827537
257	155	390	3	Handstand Hold	time	\N	\N	30	\N	\N	(♀ 65 lb) (♂ 95 lb)	95	65	1769644915.425083	1769644914.827537
258	157	402	1	chest to bar pull ups	reps	10	\N	\N	\N	\N	\N	\N	\N	1769644915.42631	1769644914.827537
195	126	43	5	Box Jumps	reps	20	\N	\N	\N	\N	\N	\N	\N	1769644915.368504	1770047268.14542
198	126	43	8	Box Jumps	reps	10	\N	\N	\N	\N	\N	\N	\N	1769644915.370841	1770047268.14542
122	134	43	2	Box Jumps	reps	20	\N	\N	\N	\N	\N	\N	\N	1769644915.287888	1770047268.14542
124	134	43	4	Box Jumps	reps	20	\N	\N	\N	\N	\N	\N	\N	1769644915.290081	1770047268.14542
142	136	43	2	Box Jumps	reps	20	\N	\N	\N	\N	\N	\N	\N	1769644915.316576	1770047268.14542
144	136	43	4	Box Jumps	reps	20	\N	\N	\N	\N	\N	\N	\N	1769644915.318531	1770047268.14542
220	141	383	2	double unders	time	\N	\N	120	\N	\N	\N	\N	\N	1769644915.392633	1770047268.14542
223	141	383	5	double unders	time	\N	\N	120	\N	\N	\N	\N	\N	1769644915.395261	1770047268.14542
226	141	383	8	double unders	time	\N	\N	120	\N	\N	\N	\N	\N	1769644915.398014	1770047268.14542
246	143	383	2	double unders	time	\N	\N	120	\N	\N	\N	\N	\N	1769644915.416111	1770047268.14542
249	143	383	5	double unders	time	\N	\N	120	\N	\N	\N	\N	\N	1769644915.418376	1770047268.14542
252	143	383	8	double unders	time	\N	\N	120	\N	\N	\N	\N	\N	1769644915.420678	1770047268.14542
237	146	6	5	Walking Lunges	reps	5	\N	\N	\N	\N	\N	\N	\N	1769644915.409278	1770047268.14542
241	146	534	9	Jumping Lunges	reps	9	\N	\N	\N	\N	\N	\N	\N	1769644915.412261	1770047268.14542
242	146	44	10	Broad Jumps	reps	10	\N	\N	\N	\N	\N	\N	\N	1769644915.412946	1770047268.14542
244	146	391	12	Single Leg Squats	reps	12	\N	\N	\N	\N	\N	\N	\N	1769644915.414297	1770047268.14542
132	148	6	5	Walking Lunges	reps	5	\N	\N	\N	\N	\N	\N	\N	1769644915.305855	1770047268.14542
136	148	534	9	Jumping Lunges	reps	9	\N	\N	\N	\N	\N	\N	\N	1769644915.310338	1770047268.14542
137	148	44	10	Broad Jumps	reps	10	\N	\N	\N	\N	\N	\N	\N	1769644915.311151	1770047268.14542
139	148	391	12	Single Leg Squats	reps	12	\N	\N	\N	\N	\N	\N	\N	1769644915.312691	1770047268.14542
256	155	59	2	L sit hold	time	\N	\N	20	\N	\N	\N	\N	\N	1769644915.424289	1770047268.14542
207	129	406	8	Kettlebell Turkish Get Ups, Left Arm	reps	4	\N	\N	\N	\N	\N	\N	\N	1769644915.378579	1769644914.827537
203	129	406	4	Kettlebell Turkish Get Ups, Left Arm	reps	5	\N	\N	\N	\N	\N	\N	\N	1769644915.375024	1769644914.827537
211	129	406	12	Kettlebell Turkish Get Ups, Left Arm	reps	3	\N	\N	\N	\N	(♀ 53-lb kettlebell) (♂ 70-lb kettlebell)	70	53	1769644915.382349	1769644914.827537
202	129	406	3	Kettlebell Turkish Get Ups, Right Arm	reps	5	\N	\N	\N	\N	\N	\N	\N	1769644915.374367	1769644914.827537
210	129	406	11	Kettlebell Turkish Get Ups, Right Arm	reps	3	\N	\N	\N	\N	\N	\N	\N	1769644915.381531	1769644914.827537
206	129	406	7	Kettlebell Turkish Get Ups, Right Arm	reps	4	\N	\N	\N	\N	\N	\N	\N	1769644915.377611	1769644914.827537
229	145	408	2	Wall Ball Shots	reps	20	\N	\N	\N	\N	\N	\N	\N	1769644915.401292	1769644914.827537
231	145	408	4	Medicine Ball To A Target	distance	\N	2	\N	\N	\N	\N	\N	14	1769644915.402982	1770048025.891026
232	145	408	5	Medicine Ball To A Target	distance	\N	3	\N	\N	\N	\N	20	\N	1769644915.404038	1770048025.891026
230	145	26	3	pull ups	reps	20	\N	\N	\N	\N	\N	\N	\N	1769644915.402131	1770047268.14542
236	146	16	4	push ups	reps	4	\N	\N	\N	\N	\N	\N	\N	1769644915.408616	1770047268.14542
131	148	16	4	push ups	reps	4	\N	\N	\N	\N	\N	\N	\N	1769644915.304533	1770047268.14542
147	153	59	2	L sit hold	time	\N	\N	20	\N	\N	\N	\N	\N	1769644915.3223	1770047268.14542
254	150	32	1	Snatches	reps	30	\N	\N	\N	\N	(♀ 95 lb) (♂ 135 lb)	135	95	1769644915.422456	1770047268.14542
212	133	400	1	Row	distance	\N	250	\N	\N	\N	\N	\N	\N	1769644915.383624	1770048025.891026
214	133	400	3	Row	distance	\N	250	\N	\N	\N	\N	\N	\N	1769644915.385709	1770048025.891026
170	119	400	1	Calorie Row	calories	30	\N	\N	30	\N	\N	\N	\N	1769644915.346727	1769644914.827537
173	119	400	4	Calorie Row	calories	24	\N	\N	24	\N	\N	\N	\N	1769644915.349154	1769644914.827537
176	119	400	7	Calorie Row	calories	18	\N	\N	18	\N	\N	\N	\N	1769644915.351501	1769644914.827537
179	119	400	10	Calorie Row	calories	12	\N	\N	12	\N	\N	\N	\N	1769644915.35391	1769644914.827537
182	119	400	13	Calorie Row	calories	6	\N	\N	6	\N	\N	\N	\N	1769644915.356397	1769644914.827537
239	146	131	7	Sit-Ups	reps	7	\N	\N	\N	\N	\N	\N	\N	1769644915.41082	1769644914.827537
243	146	501	11	handstand push ups	reps	11	\N	\N	\N	\N	\N	\N	\N	1769644915.413633	1770047268.14542
138	148	501	11	handstand push ups	reps	11	\N	\N	\N	\N	\N	\N	\N	1769644915.311922	1770047268.14542
\.


--
-- Data for Name: equipment; Type: TABLE DATA; Schema: public; Owner: jacked
--

COPY public.equipment (id, name) FROM stdin;
211	none
212	machine
213	other
214	foam roll
215	cable
216	band
217	pull_up_bar
218	ab_wheel
219	plyo_box
221	medicine_ball
222	kettlebell
223	barbell
224	rack
225	dumbbell
226	bench
227	dip_station
228	rings
229	parallettes
230	wall
231	battle_rope
232	trap_bar
233	sled
235	ez curl bar
237	exercise ball
238	box
240	rowing_machine
242	wall_ball
243	sandbag
\.


--
-- Data for Name: equipment_backup_20260301; Type: TABLE DATA; Schema: public; Owner: jacked
--

COPY public.equipment_backup_20260301 (id, name) FROM stdin;
211	none
212	machine
213	other
214	foam roll
215	cable
216	band
217	pull_up_bar
218	ab_wheel
219	plyo_box
221	medicine_ball
222	kettlebell
223	barbell
224	rack
225	dumbbell
226	bench
227	dip_station
228	rings
229	parallettes
230	wall
231	battle_rope
232	trap_bar
233	sled
235	ez curl bar
237	exercise ball
238	box
240	rowing_machine
242	wall_ball
243	sandbag
\.


--
-- Data for Name: hyrox_scraping_log; Type: TABLE DATA; Schema: public; Owner: jacked
--

COPY public.hyrox_scraping_log (id, scrape_session_id, started_at, completed_at, total_workouts_found, workouts_scraped, workouts_saved, errors_count, has_errors, notes, created_at) FROM stdin;
1	1772312993.966245	2026-02-28 21:09:54.048749+00	2026-02-28 21:09:54.048749+00	5	5	5	0	f	Initial test scrape from wodwell.com	2026-02-28 21:09:54.048749+00
\.


--
-- Data for Name: hyrox_scraping_log_staging; Type: TABLE DATA; Schema: public; Owner: jacked
--

COPY public.hyrox_scraping_log_staging (id, scrape_session_id, started_at, completed_at, total_workouts_found, workouts_scraped, workouts_saved, errors_count, has_errors, error_summary, user_agent, notes) FROM stdin;
2	1772312993.966245	2026-02-28 21:09:54.048749	2026-02-28 21:09:54.048749	5	5	5	0	f	\N	\N	Initial test scrape from wodwell.com
\.


--
-- Data for Name: hyrox_workout_lines; Type: TABLE DATA; Schema: public; Owner: jacked
--

COPY public.hyrox_workout_lines (id, workout_id, line_text, line_number, is_rest, movement_name, reps, distance_meters, duration_seconds, weight_text, calories, movement_id, created_at, updated_at) FROM stdin;
1	1	40 second Max Wall Ball Shots (20/14 lb)	3	f	Wall ball shots	40	\N	40	M:20.00/F:14.00	\N	\N	2026-02-28 22:33:51.501038+00	2026-02-28 22:33:51.501038+00
2	1	20 second Rest	4	f	Rest	20	\N	20	\N	\N	\N	2026-02-28 22:33:51.501038+00	2026-02-28 22:33:51.501038+00
3	1	20 second Rest	6	f	Rest	20	\N	20	\N	\N	\N	2026-02-28 22:33:51.501038+00	2026-02-28 22:33:51.501038+00
4	1	20 second Rest	8	f	Rest	20	\N	20	\N	\N	\N	2026-02-28 22:33:51.501038+00	2026-02-28 22:33:51.501038+00
5	1	40 second Max Burpees	9	f	Burpees	40	\N	40	\N	\N	\N	2026-02-28 22:33:51.501038+00	2026-02-28 22:33:51.501038+00
6	1	20 second Rest	10	f	Rest	20	\N	20	\N	\N	\N	2026-02-28 22:33:51.501038+00	2026-02-28 22:33:51.501038+00
7	1	20 second Rest	12	f	Rest	20	\N	20	\N	\N	\N	2026-02-28 22:33:51.501038+00	2026-02-28 22:33:51.501038+00
8	2	400 meter Run	2	f	Run	400	400	\N	\N	\N	\N	2026-02-28 22:33:51.56724+00	2026-02-28 22:33:51.56724+00
9	2	20 Burpees	3	f	20 burpees	20	\N	\N	\N	\N	\N	2026-02-28 22:33:51.56724+00	2026-02-28 22:33:51.56724+00
10	2	600 meter Run	4	f	Run	600	600	\N	\N	\N	\N	2026-02-28 22:33:51.56724+00	2026-02-28 22:33:51.56724+00
11	2	40 Wall Ball Shots (20/14 lb)	5	f	40 wall ball shots	40	\N	\N	M:20.00/F:14.00	\N	\N	2026-02-28 22:33:51.56724+00	2026-02-28 22:33:51.56724+00
12	2	800 meter Run	6	f	Run	800	800	\N	\N	\N	\N	2026-02-28 22:33:51.56724+00	2026-02-28 22:33:51.56724+00
13	2	1,000 meter Run	8	f	Run	1	0	\N	\N	\N	\N	2026-02-28 22:33:51.56724+00	2026-02-28 22:33:51.56724+00
14	2	800 meter Run	10	f	Run	800	800	\N	\N	\N	\N	2026-02-28 22:33:51.56724+00	2026-02-28 22:33:51.56724+00
15	2	40 Wall Ball Shots (20/14 lb)	11	f	40 wall ball shots	40	\N	\N	M:20.00/F:14.00	\N	\N	2026-02-28 22:33:51.56724+00	2026-02-28 22:33:51.56724+00
16	2	600 meter Run	12	f	Run	600	600	\N	\N	\N	\N	2026-02-28 22:33:51.56724+00	2026-02-28 22:33:51.56724+00
17	2	20 Burpees	13	f	20 burpees	20	\N	\N	\N	\N	\N	2026-02-28 22:33:51.56724+00	2026-02-28 22:33:51.56724+00
18	2	400 meter Run	14	f	Run	400	400	\N	\N	\N	\N	2026-02-28 22:33:51.56724+00	2026-02-28 22:33:51.56724+00
19	3	400 meter Row	2	f	Row	400	400	\N	\N	\N	\N	2026-02-28 22:33:51.623811+00	2026-02-28 22:33:51.623811+00
20	3	30 Wall Ball Shots (20/14 lb)	3	f	30 wall ball shots	30	\N	\N	M:20.00/F:14.00	\N	\N	2026-02-28 22:33:51.623811+00	2026-02-28 22:33:51.623811+00
21	3	400 meter Run	4	f	Run	400	400	\N	\N	\N	\N	2026-02-28 22:33:51.623811+00	2026-02-28 22:33:51.623811+00
22	3	30 Burpees	5	f	30 burpees	30	\N	\N	\N	\N	\N	2026-02-28 22:33:51.623811+00	2026-02-28 22:33:51.623811+00
23	3	400 meter Row	6	f	Row	400	400	\N	\N	\N	\N	2026-02-28 22:33:51.623811+00	2026-02-28 22:33:51.623811+00
24	3	400 meter Run	8	f	Run	400	400	\N	\N	\N	\N	2026-02-28 22:33:51.623811+00	2026-02-28 22:33:51.623811+00
25	3	30 Hand Release Push-Ups	9	f	30 hand release push-ups	30	\N	\N	\N	\N	\N	2026-02-28 22:33:51.623811+00	2026-02-28 22:33:51.623811+00
26	3	400 meter Row	10	f	Row	400	400	\N	\N	\N	\N	2026-02-28 22:33:51.623811+00	2026-02-28 22:33:51.623811+00
27	3	100 meter Farmer's Carry (2x50/35 lb)	11	f	Farmer's carry	100	100	\N	\N	\N	\N	2026-02-28 22:33:51.623811+00	2026-02-28 22:33:51.623811+00
28	3	400 meter Run	12	f	Run	400	400	\N	\N	\N	\N	2026-02-28 22:33:51.623811+00	2026-02-28 22:33:51.623811+00
29	4	5 Burpees	4	f	5 burpees	5	\N	\N	\N	\N	\N	2026-02-28 22:33:51.701034+00	2026-02-28 22:33:51.701034+00
30	4	10 Wall Ball Shots (20/14 lb)	5	f	10 wall ball shots	10	\N	\N	M:20.00/F:14.00	\N	\N	2026-02-28 22:33:51.701034+00	2026-02-28 22:33:51.701034+00
31	4	15 calorie Row	6	f	Row	15	\N	\N	\N	15	\N	2026-02-28 22:33:51.701034+00	2026-02-28 22:33:51.701034+00
32	4	30 meter Farmer's Carry (2x50/35 lb)	9	f	Farmer's carry	30	30	\N	\N	\N	\N	2026-02-28 22:33:51.701034+00	2026-02-28 22:33:51.701034+00
33	5	20 Push-Ups	3	f	20 push-ups	20	\N	\N	\N	\N	\N	2026-02-28 22:33:51.808082+00	2026-02-28 22:33:51.808082+00
34	5	40 calorie Row	5	f	Row	40	\N	\N	\N	40	\N	2026-02-28 22:33:51.808082+00	2026-02-28 22:33:51.808082+00
35	5	10 Burpee Broad Jumps	2	f	10 burpee broad jumps	10	\N	\N	\N	\N	712	2026-02-28 22:33:51.808082+00	2026-02-28 22:33:51.808082+00
36	1	40 second Max Calorie Ski Erg	5	f	Calorie ski erg	40	\N	40	\N	\N	713	2026-02-28 22:33:51.501038+00	2026-02-28 22:33:51.501038+00
37	1	40 second Max V-Ups	11	f	V-ups	40	\N	40	\N	\N	714	2026-02-28 22:33:51.501038+00	2026-02-28 22:33:51.501038+00
38	3	100 Sit-Ups	13	f	100 sit-ups	100	\N	100	\N	\N	715	2026-02-28 22:33:51.623811+00	2026-02-28 22:33:51.623811+00
39	4	25 Sit-Ups	8	f	25 sit-ups	25	\N	25	\N	\N	715	2026-02-28 22:33:51.701034+00	2026-02-28 22:33:51.701034+00
40	2	60 Sandbag Lunges (60/40 lb)	7	f	60 sandbag lunges	60	\N	60	M:60.00/F:40.00	\N	716	2026-02-28 22:33:51.56724+00	2026-02-28 22:33:51.56724+00
41	2	60 Sandbag Lunges (60/40 lb)	9	f	60 sandbag lunges	60	\N	60	M:60.00/F:40.00	\N	716	2026-02-28 22:33:51.56724+00	2026-02-28 22:33:51.56724+00
42	3	30 Sandbag Lunges (60/40 lb)	7	f	30 sandbag lunges	30	\N	30	M:60.00/F:40.00	\N	716	2026-02-28 22:33:51.623811+00	2026-02-28 22:33:51.623811+00
43	4	20 Sandbag Lunges (60/40 lb)	7	f	20 sandbag lunges	20	\N	20	M:60.00/F:40.00	\N	716	2026-02-28 22:33:51.701034+00	2026-02-28 22:33:51.701034+00
44	5	30 Sandbag Lunges (60/40 lb)	4	f	30 sandbag lunges	30	\N	30	M:60.00/F:40.00	\N	716	2026-02-28 22:33:51.808082+00	2026-02-28 22:33:51.808082+00
45	1	40 second Max Lunges	7	f	Lunges	40	\N	40	\N	\N	717	2026-02-28 22:33:51.501038+00	2026-02-28 22:33:51.501038+00
\.


--
-- Data for Name: hyrox_workout_movements_staging; Type: TABLE DATA; Schema: public; Owner: jacked
--

COPY public.hyrox_workout_movements_staging (id, workout_id, line_id, movement_name, movement_type, reps, distance_meters, duration_seconds, calories, weight_male, weight_female, is_max_effort, notes, created_at) FROM stdin;
\.


--
-- Data for Name: hyrox_workout_tags; Type: TABLE DATA; Schema: public; Owner: jacked
--

COPY public.hyrox_workout_tags (id, workout_id, tag_name, created_at) FROM stdin;
1	1	Hyrox Workout of Week	2026-02-28 22:33:51.464263+00
2	2	Hyrox Workout of Week	2026-02-28 22:33:51.53297+00
3	3	Hyrox Workout of Week	2026-02-28 22:33:51.601317+00
4	4	Hyrox Workout of Week	2026-02-28 22:33:51.6514+00
5	5	Hyrox Workout of Week	2026-02-28 22:33:51.766686+00
\.


--
-- Data for Name: hyrox_workouts; Type: TABLE DATA; Schema: public; Owner: jacked
--

COPY public.hyrox_workouts (id, wod_id, name, url, badge, workout_type, workout_goal, time_specification, total_time_minutes, time_cap_minutes, has_buy_in, has_cash_out, is_complex, background_image, favorites_count, comments_count, full_description, source_page, created_at, updated_at) FROM stdin;
1	beverly-hills	Beverly Hills	https://wodwell.com/wod/beverly-hills/	Hyrox Workout of Week	amrap	mixed	\N	\N	25	f	f	f	\N	0	0	AMRAP in 25 minutes\nComplete 5 rounds of:\n40 second Max Wall Ball Shots (20/14 lb)\n20 second Rest\n40 second Max Calorie Ski Erg\n20 second Rest\n40 second Max Lunges\n20 second Rest\n40 second Max Burpees\n20 second Rest\n40 second Max V-Ups\n20 second Rest	\N	2026-02-28 22:17:12.200578+00	2026-02-28 22:17:12.200578+00
2	wyck	Wyck	https://wodwell.com/wod/wyck/	Hyrox Workout of Week	for_time	finish_quickly	\N	\N	\N	f	f	f	\N	0	0	For Time\n400 meter Run\n20 Burpees\n600 meter Run\n40 Wall Ball Shots (20/14 lb)\n800 meter Run\n60 Sandbag Lunges (60/40 lb)\n1,000 meter Run\n60 Sandbag Lunges (60/40 lb)\n800 meter Run\n40 Wall Ball Shots (20/14 lb)\n600 meter Run\n20 Burpees\n400 meter Run	\N	2026-02-28 22:17:12.229198+00	2026-02-28 22:17:12.229198+00
3	bordesley	Bordesley	https://wodwell.com/wod/bordesley/	Hyrox Workout of Week	for_time	finish_quickly	\N	\N	\N	f	f	f	\N	0	0	For Time\n400 meter Row\n30 Wall Ball Shots (20/14 lb)\n400 meter Run\n30 Burpees\n400 meter Row\n30 Sandbag Lunges (60/40 lb)\n400 meter Run\n30 Hand Release Push-Ups\n400 meter Row\n100 meter Farmer's Carry (2x50/35 lb)\n400 meter Run\n100 Sit-Ups	\N	2026-02-28 22:17:12.266564+00	2026-02-28 22:17:12.266564+00
4	telliskivi	Telliskivi	https://wodwell.com/wod/telliskivi/	Hyrox Workout of Week	for_time	finish_quickly	\N	\N	\N	t	t	t	\N	0	0	For Time\nBuy-In: 1,000 meter Run\nThen, AMRAP in 35 minutes:\n5 Burpees\n10 Wall Ball Shots (20/14 lb)\n15 calorie Row\n20 Sandbag Lunges (60/40 lb)\n25 Sit-Ups\n30 meter Farmer's Carry (2x50/35 lb)\nCash-Out: 1,000 meter Run	\N	2026-02-28 22:17:12.292821+00	2026-02-28 22:17:12.292821+00
5	changning	Changning	https://wodwell.com/wod/changning/	Hyrox Workout of Week	amrap	mixed	\N	\N	30	f	f	f	\N	0	0	AMRAP in 30 minutes\n10 Burpee Broad Jumps\n20 Push-Ups\n30 Sandbag Lunges (60/40 lb)\n40 calorie Row	\N	2026-02-28 22:17:12.311539+00	2026-02-28 22:17:12.311539+00
\.


--
-- Data for Name: migration_version; Type: TABLE DATA; Schema: public; Owner: jacked
--

COPY public.migration_version (version, description, applied_at, checksum) FROM stdin;
migrations-20260227133538	migrations.sql	2026-02-27 12:35:38.087421	802a4e5d138233f922d100a9d0963127
\.


--
-- Data for Name: movement_coaching_cues; Type: TABLE DATA; Schema: public; Owner: jacked
--

COPY public.movement_coaching_cues (id, movement_id, cue_text, "order") FROM stdin;
7349	256	Repeat for the desired number of repetitions.	4
6589	72	Lie on the floor with the knees bent and the feet on the floor around 18-24 inches apart. Your arms should be extended by your side. This will be your starting position.	0
6590	72	Crunch over your torso forward and up about 3-4 inches to the right side and touch your right heel as you hold the contraction for a second. Exhale while performing this movement.	1
6591	72	Now go back slowly to the starting position as you inhale.	2
6592	72	Now crunch over your torso forward and up around 3-4 inches to the left side and touch your left heel as you hold the contraction for a second. Exhale while performing this movement and then go back to the starting position as you inhale. Now that both heels have been touched, that is considered 1 repetition.	3
6593	72	Continue alternating sides in this manner until all prescribed repetitions are done.	4
6596	75	Begin seated on the ground with your legs bent and your feet on the floor.	0
6597	75	Using a Muscle Roller or a rolling pin, apply pressure to the muscles on the outside of your shins. Work from just below the knee to above the ankle, pausing at points of tension for 10-30 seconds. Repeat on the other leg.	1
6598	76	Stand up and extend your arms straight out by the sides. The arms should be parallel to the floor and perpendicular (90-degree angle) to your torso. This will be your starting position.	0
6599	76	Slowly start to make circles of about 1 foot in diameter with each outstretched arm. Breathe normally as you perform the movement.	1
6600	76	Continue the circular motion of the outstretched arms for about ten seconds. Then reverse the movement, going the opposite direction.	2
6601	123	Get on your hands and knees, walk your hands in front of you.	0
6602	123	Lower your buttocks down to sit on your heels. Let your arms drag along the floor as you sit back to stretch your entire spine.	1
6603	123	Once you settle onto your heels, bring your hands next to your feet and relax. breathe into your back. Rest your forehead on the floor. Avoid this position if you have knee problems.	2
6604	227	Start off by lying on the floor.	0
6605	227	Extend one leg straight and pull the other knee to your chest. Hold under the knee joint to protect the kneecap.	1
6606	227	Gently tug that knee toward your nose.	2
6607	227	Switch sides. This stretches the buttocks and lower back of the bent leg and the hip flexor of the straight leg.	3
6608	228	Lie down with your feet on the floor, heels directly under your knees.	0
6609	228	Lift only your tailbone to the ceiling to stretch your lower back. (Don't lift the entire spine yet.) Pull in your stomach.	1
6610	228	To go into a bridge, lift the entire spine except the neck.	2
6613	231	Sit with your buttocks on top of a foam roll. Bend your knees, and then cross one leg so that the ankle is over the knee. This will be your starting position.	0
6614	231	Shift your weight to the side of the crossed leg, rolling over the buttocks until you feel tension in your upper glute. You may assist the stretch by using one hand to pull the bent knee towards your chest. Hold this position for 10-30 seconds, and then switch sides.	1
6615	245	Lay facedown on the floor with your weight supported by your hands or forearms. Place a foam roll underneath one leg on the quadriceps, and keep the foot off of the ground. Make sure to relax the leg as much as possible. This will be your starting position.	0
6616	245	Shifting as much weight onto the leg to be stretched as is tolerable, roll over the foam from above the knee to below the hip, holding points of tension for 10-30 seconds. Switch sides.	1
6617	259	Lay down with your back on the floor. Place a foam roll underneath your upper back, and cross your arms in front of you, protracting your shoulders. This will be your starting position.	0
6618	259	Raise your hips off of the ground, placing your weight onto the foam roll. Shift your weight to one side at a time, rolling over your middle and upper back. Pause at points of tension for 10-30 seconds.	1
6619	269	Sit on the floor with your knees bent and your partner standing behind you. Extend your arms straight behind you with your palms facing each other. Your partner will hold your wrists for you. This will be the starting position.	0
6620	269	Attempt to flex your elbows, while your partner prevents any actual movement.	1
6621	269	After 10-20 seconds, relax your arms while your partner gently pulls your wrists up to stretch your biceps. Be sure to let your partner know when the stretch is appropriate to prevent injury or overstretching.	2
6622	270	In a seated position with your knees bent, cross one ankle over the opposite knee. Your partner will stand behind you. Now, lean forward as your partner braces your shoulders with their hands. This will be your starting position.	0
6623	270	Attempt to push your torso back for 10-20 seconds, as your partner prevents any actual movement of your torso.	1
6624	270	Now relax your muscles as your partner increases the stretch by gently pushing your torso forward for 10-20 seconds.	2
6628	294	Stand with some space in front and behind you.	0
6629	294	Bend at the waist, keeping your legs straight, until you can relax and let your upper body hang down in front of you. Let your arms and hands hang down naturally. Hold for 10 to 20 seconds.	1
6630	216	Lie flat on the floor with your lower back pressed to the ground. For this exercise, you will need to put one hand beside your head and the other to the side against the floor.	0
6631	216	Make sure your feet are elevated and resting on a flat surface.	1
6632	216	Now lift the shoulder in which your hand is touching your head.	2
6633	216	Simply elevate your shoulder and body upward until you touch your knee. For example, if you have your right hand besides your head, then you want to elevate your body upwards until your right elbow touches your left knee. The same variation can be applied doing the inverse and using your left elbow to touch your right knee.	3
6634	216	After your knee touches your elbow, lower your body until you have reached the starting position.	4
6635	216	Remember to breathe in during the eccentric (lowering) part of the exercise and to breathe out during the concentric (upward) part of the exercise.	5
6636	216	Continue alternating in this manner until all of the recommended repetitions for each side have been completed.	6
6642	297	To begin, stand straight with your feet shoulder width apart from each other. Place your hands on your hips. This is the starting position.	0
6643	297	Now slowly inhale as much air as possible and then start to exhale as much as possible while bringing your stomach in as much as possible and hold this position. Try to visualize your navel touching your backbone.	1
6644	297	One isometric contraction is around 20 seconds. During the 20 second hold, try to breathe normally. Then inhale and bring your stomach back to the starting position.	2
6645	297	Once you have practiced this exercise, try to perform this exercise for longer than 20 seconds. Tip: You can work your way up to 40-60 seconds.	3
6646	297	Repeat for the recommended amount of sets.	4
6647	299	To begin, lie straight and face down on the floor or exercise mat. Your arms should be fully extended in front of you. This is the starting position.	0
6648	299	Simultaneously raise your arms, legs, and chest off of the floor and hold this contraction for 2 seconds. Tip: Squeeze your lower back to get the best results from this exercise. Remember to exhale during this movement. Note: When holding the contracted position, you should look like superman when he is flying.	1
6649	299	Slowly begin to lower your arms, legs and chest back down to the starting position while inhaling.	2
6650	299	Repeat for the recommended amount of repetitions prescribed in your program.	3
6651	305	Begin in a seated, upright position. Start by extending your legs in front of you in a V.	0
6652	305	With your hands on the floor, lean forward as far as possible. Hold for 10 to 20 seconds.	1
6653	309	To begin, lie down on the floor or an exercise mat with your back pressed against the floor. Your arms should be lying across your sides with the palms facing down.	0
6654	309	Your legs should be touching each other. Slowly elevate your legs up in the air until they are almost perpendicular to the floor with a slight bend at the knees. Your feet should be parallel to the floor.	1
6655	309	Move your arms so that they are fully extended at a 45 degree angle from the floor. This is the starting position.	2
6656	309	While keeping your lower back pressed against the floor, slowly lift your torso and use your hands to try and touch your toes. Remember to exhale while perform this part of the exercise.	3
6657	309	Slowly begin to lower your torso and arms back down to the starting position while inhaling. Remember to keep your arms straight out pointing towards your toes.	4
6658	309	Repeat for the recommended amount of repetitions.	5
6662	319	Start by standing straight with your feet being shoulder width apart from each other. Elevate your arms to the side of you until they are fully extended and parallel to the floor at a height that is evenly aligned with your shoulders. Tip: Your torso and arms should form the letter T: Your palms should be facing down. This is the starting position.	0
6789	85	Extend as far as possible, then reverse the motion to return to the starting position.	2
6663	319	Keeping your entire body stationary except for the wrists, begin to rotate both wrists forward in a circular motion. Tip: Pretend that you are trying to draw circles by using your hands as the brush. Breathe normally as you perform this exercise.	1
6664	319	Repeat for the recommended amount of repetitions.	2
6665	324	Start off on your hands and knees, then lift your leg off the floor and hold the foot with your hand.	0
6666	324	Use your hand to hold the foot or ankle, keeping the knee fully flexed, stretching the quadriceps and hip flexors.	1
6667	324	Focus on extending your hips, thrusting them towards the floor. Hold for 10-20 seconds and then switch sides.	2
6668	330	Sit upright in a chair and grip the seat on the sides.	0
6669	330	Raise one leg, extending the knee, flexing the ankle as you do so.	1
6670	330	Slowly move that leg outward as far as you can, and then back to the center and down.	2
6671	330	Repeat for your other leg.	3
6672	332	Sit on the edge of a chair, gripping the back of it.	0
6673	332	Straighten your arms, keeping your back straight, and pull your upper body forward so you feel a stretch. Hold for 20-30 seconds.	1
6659	186	Lie on your back with your arms extended out to the sides and your legs straight. This will be your starting position.	0
6660	186	Lift one leg and quickly cross it over your body, attempting to touch the ground near the opposite hand.	1
6661	186	Return to the starting position, and repeat with the opposite leg. Continue to alternate for 10-20 repetitions.	2
6674	334	Stand with your feet shoulder width apart. This will be your starting position.	0
6675	334	Keeping your arms straight, swing them straight up in front of you 5-10 times, increasing the range of motion each time until your arms are above your head.	1
6676	335	Stand up straight.	0
6677	335	Place both hands on your lower back, fingers pointing downward and elbows out.	1
6678	335	Then gently pull your elbows back aiming to touch them together.	2
6679	339	Lie on your back with your legs extended. Loop a belt, rope, or band around one of your feet, and swing that leg as far to the side as you can. This will be your starting position.	0
6680	339	Pull gently on the belt to create tension in your groin and hamstring muscles. Hold for 10-20 seconds, and repeat on the other side.	1
6681	348	Lie on a flat bench or step, and hang one leg and arm over the side.	0
6682	348	Bend the knee and hold the top of the foot. As you do this, be careful not to arch your lower back.	1
6683	348	Pull the belly button to the spine to stay in neutral. Press your foot down and into your hand. To add the hip stretch, lift the hip of the leg you're holding up toward the ceiling.	2
6684	348	Switch sides.	3
6685	349	Start off by lying on your right side, with your right knee bent at a 90-degree angle resting on the floor in front of you (this stabilizes the torso).	0
6686	349	Bend your left knee behind you and hold your left foot with your left hand. To stretch your hip flexor, press your left hip forward as you push your left foot back into your hand. Switch sides.	1
6687	358	Sit upright on the floor with your legs bent, your partner standing behind you. Stick your arms straight out to your sides, with your palms facing the ground. Attempt to move them as far behind you as possible, as your assistant holds your wrists. This will be your starting position.	0
6688	358	Keeping your elbows straight, attempt to move your arms to the front, with your partner gently restraining you to prevent any actual movement for 10-20 seconds.	1
6689	358	Now, relax your muscles and allow your partner to gently increase the stretch on the shoulders and chest. Hold for 10 to 20 seconds.	2
6690	369	While seated, bend forward to hug your thighs from underneath with both arms.	0
6691	369	Keep your knees together and your legs extended out as you bring your chest down to your knees. You can also stretch your middle back by pulling your back away from your knees as your hugging them.	1
6692	370	Clasp fingers together with your thumbs pointing down, round your shoulders as you reach your hands forward.	0
6693	371	This is a three-part stretch. Begin by lunging forward, with your front foot flat on the ground and on the toes of your back foot. With your knees bent, squat down until your knee is almost touching the ground. Keep your torso erect, and hold this position for 10-20 seconds.	0
6694	371	Now, place the arm on the same side as your front leg on the ground, with the elbow next to the foot. Your other hand should be placed on the ground, parallel to your lead leg, to help support you during this portion of the stretch.	1
6695	371	After 10-20 seconds, place your hands on either side of your front foot. Raise the toes of the front foot off of the ground, and straighten your leg. You may need to reposition your rear leg to do so. Hold for 10-20 seconds, and then repeat the entire sequence for the other side.	2
6696	235	Place a kettlebell on the floor. Place yourself in a pushup position, on your toes with one hand on the ground and one hand holding the kettlebell, with your elbows extended. This will be your starting position.	0
6697	235	Begin by lowering yourself as low as you can, keeping your back straight.	1
6698	235	Quickly and forcefully reverse direction, pushing yourself up to the other side of the kettlebell, switching hands as you do so. Continue the movement by descending and repeating the movement back and forth.	2
6701	341	Begin in a comfortable standing position with your knees slightly bent. Hold your hands in front of you, palms down with your fingertips together at chest height. This will be your starting position.	0
6702	341	Rapidly dip down into a quarter squat and immediately explode upward. Drive the knees towards the chest, attempting to touch them to the palms of the hands.	1
6703	341	Jump as high as you can, raising your knees up, and then ensure a good land be re-extending your legs, absorbing impact through be allowing the knees to rebend.	2
6704	152	To begin, step onto the elliptical and select the desired option from the menu. Most ellipticals have a manual setting, or you can select a program to run. Typically, you can enter your age and weight to estimate the amount of calories burned during exercise. Elevation can be adjusted to change the intensity of the workout.	0
6705	152	The handles can be used to monitor your heart rate to help you stay at an appropriate intensity.	1
6706	180	To begin, step onto the treadmill and select the desired option from the menu. Most treadmills have a manual setting, or you can select a program to run. Typically, you can enter your age and weight to estimate the amount of calories burned during exercise. Elevation can be adjusted to change the intensity of the workout.	0
6707	180	Treadmills offer convenience, cardiovascular benefits, and usually have less impact than jogging outside. A 150 lb person will burn almost 250 calories jogging for 30 minutes, compared to more than 450 calories running. Maintain proper posture as you jog, and only hold onto the handles when necessary, such as when dismounting or checking your heart rate.	1
6708	289	To begin, step onto the stairmaster and select the desired option from the menu. You can choose a manual setting, or you can select a program to run. Typically, you can enter your age and weight to estimate the amount of calories burned during exercise.	0
6709	289	Pump your legs up and down in an established rhythm, driving the pedals down but not all the way to the floor. It is recommended that you maintain your grip on the handles so that you don fall. The handles can be used to monitor your heart rate to help you stay at an appropriate intensity.	1
7014	154	Skip by executing a step-hop pattern of right-right-step to left-left-step, and so on, alternating back and forth.	1
6710	289	Stairmasters offer convenience, cardiovascular benefits, and usually have less impact than running outside. They are typically much harder than other cardio equipment. A 150 lb person will typically burn over 300 calories in 30 minutes, compared to about 175 calories walking.	2
6711	296	To begin, step onto the stepmill and select the desired option from the menu. You can choose a manual setting, or you can select a program to run. Typically, you can enter your age and weight to estimate the amount of calories burned during exercise. Use caution so that you don trip as you climb the stairs. It is recommended that you maintain your grip on the handles so that you don fall.	0
6712	296	Stepmills offer convenience, cardiovascular benefits, and usually have less impact than running outside while offering a similar rate of calories burned. They are typically much harder than other cardio equipment. A 150 lb person will typically burn over 300 calories in 30 minutes, compared to about 175 calories walking.	1
7033	159	Slowly start going back to the starting position as you inhale.	4
6713	101	Lie flat on the floor on your back with the hands by your side and your knees bent. Your feet should be placed around shoulder width. This will be your starting position.	0
6714	101	Pushing mainly with your heels, lift your hips off the floor while keeping your back straight. Breathe out as you perform this part of the motion and hold at the top for a second.	1
6715	101	Slowly go back to the starting position as you breathe in.	2
6716	103	Kneel below a high pulley that contains a rope attachment.	0
6717	103	Grasp cable rope attachment and lower the rope until your hands are placed next to your face.	1
6718	103	Flex your hips slightly and allow the weight to hyperextend the lower back. This will be your starting position.	2
6719	103	With the hips stationary, flex the waist as you contract the abs so that the elbows travel towards the middle of the thighs. Exhale as you perform this portion of the movement and hold the contraction for a second.	3
6720	103	Slowly return to the starting position as you inhale. Tip: Make sure that you keep constant tension on the abs throughout the movement. Also, do not choose a weight so heavy that the lower back handles the brunt of the work.	4
6721	103	Repeat for the recommended amount of repetitions.	5
6722	104	Move the cables to the bottom of the towers and select an appropriate weight. Stand directly in between the uprights.	0
6723	104	To begin, squat down be flexing your hips and knees until you can reach the handles.	1
6724	104	After grasping them, begin your ascent. Driving through your heels extend your hips and knees keeping your hands hanging at your side. Keep your head and chest up throughout the movement.	2
6725	104	After reaching a full standing position, Return to the starting position and repeat.	3
6726	109	Connect an ankle strap attachment to a low pulley cable and position a mat on the floor in front of it.	0
6727	109	Sit down with your feet toward the pulley and attach the cable to your ankles.	1
6728	109	Lie down, elevate your legs and bend your knees at a 90-degree angle. Your legs and the cable should be aligned. If not, adjust the pulley up or down until they are.	2
6729	109	With your hands behind your head, bring your knees inward to your torso and elevate your hips off the floor.	3
6730	109	Pause for a moment and in a slow and controlled manner drop your hips and bring your legs back to the starting 90-degree angle. You should still have tension on your abs in the resting position.	4
6731	109	Repeat the same movement to failure.	5
6732	127	With the weight loaded, take a zurcher hold on the end of the implement. Place the bar in the crook of the elbow and hold onto your wrist. Try to keep the weight off of the forearms.	0
6733	127	Begin by lifting the weight from the ground. Keep a tight, upright posture as you being to walk, taking short, fast steps. Look up and away as you turn in a circle. Do not hold your breath during the event. Continue walking until you complete one or more complete turns.	1
6738	67	Select a light resistance and sit down on the ab machine placing your feet under the pads provided and grabbing the top handles. Your arms should be bent at a 90 degree angle as you rest the triceps on the pads provided. This will be your starting position.	0
6739	67	At the same time, begin to lift the legs up as you crunch your upper torso. Breathe out as you perform this movement. Tip: Be sure to use a slow and controlled motion. Concentrate on using your abs to move the weight while relaxing your legs and feet.	1
6740	67	After a second pause, slowly return to the starting position as you breathe in.	2
6741	67	Repeat the movement for the prescribed amount of repetitions.	3
6742	70	Clean and press a kettlebell overhead with one arm.	0
6788	85	Begin the movement by driving through with your heels, extending your hips vertically through the bar. Your weight should be supported by your upper back and the heels of your feet.	1
6743	70	Keeping the kettlebell locked out at all times, push your butt out in the direction of the locked out kettlebell. Keep the non-working arm behind your back and turn your feet out at a forty-five degree angle from the arm with the kettlebell.	1
6744	70	Lower yourself as far as possible.	2
6745	70	Pause for a second and reverse the motion back to the starting position.	3
6746	71	Lie flat on the floor with your lower back pressed to the ground. For this exercise, you will need to put your hands beside your head. Be careful however to not strain with the neck as you perform it. Now lift your shoulders into the crunch position.	0
6747	71	Bring knees up to where they are perpendicular to the floor, with your lower legs parallel to the floor. This will be your starting position.	1
6748	71	Now simultaneously, slowly go through a cycle pedal motion kicking forward with the right leg and bringing in the knee of the left leg. Bring your right elbow close to your left knee by crunching to the side, as you breathe out.	2
6749	71	Go back to the initial position as you breathe in.	3
6750	71	Crunch to the opposite side as you cycle your legs and bring closer your left elbow to your right knee and exhale.	4
6751	71	Continue alternating in this manner until all of the recommended repetitions for each side have been completed.	5
6752	73	Use a sturdy object like a squat rack to hold yourself.	0
6753	73	Lift the right leg in the air (just around 2 inches from the floor) and perform a circular motion with the big toe. Pretend that you are drawing a big circle with it. Tip: One circle equals 1 repetition. Breathe normally as you perform the movement.	1
6754	73	When you are done with the right foot, then repeat with the left leg.	2
6755	77	Lay down on a flat bench holding a dumbbell in each hand with the palms of the hands facing towards the ceiling. Tip: Your arms should be parallel to the floor and next to your thighs. To avoid injury, make sure that you keep your elbows slightly bent. This will be your starting position.	0
6756	77	Now move the dumbbells by creating a semi-circle as you displace them from the initial position to over the head. All of the movement should happen with the arms parallel to the floor at all times. Breathe in as you perform this portion of the movement.	1
6757	77	Reverse the movement to return the weight to the starting position as you exhale.	2
6758	78	This trainer is effective for developing Atlas Stone strength for those who don't have access to stones, and are typically made from bar ends or heavy pipe.	0
7034	159	Repeat for the recommended amount of repetitions.	5
6759	78	Begin by loading the desired weight onto the bar. Straddle the weight, wrapping your arms around the implement, bending at the hips.	1
6760	78	Begin by pulling the weight up past the knees, extending through the hips. As the weight clears the knees, it can be lapped by resting it on your thighs and sitting back, hugging it tightly to your chest.	2
6761	78	Finish the movement by extending through your hips and knees to raise the weight as high as possible. The weight can be returned to the lap or to the ground for successive repetitions.	3
6762	79	Begin with the atlas stone between your feet. Bend at the hips to wrap your arms vertically around the Atlas Stone, attempting to get your fingers underneath the stone. Many stones will have a small flat portion on the bottom, which will make the stone easier to hold.	0
6763	79	Pulling the stone into your torso, drive through the back half of your feet to pull the stone from the ground.	1
6764	79	As the stone passes the knees, lap it by sitting backward, pulling the stone on top of your thighs.	2
6765	79	Sit low, getting the stone high onto your chest as you change your grip to reach over the stone. Stand, driving through with your hips. Close distance to the loading platform, and lean back, extending the hips to get the stone as high as possible.	3
6766	74	From a lying position, bend your knees and keep your feet on the floor.	0
6767	74	Place your ankle of one foot on your opposite knee.	1
6768	74	Grasp the thigh or knee of the bottom leg and pull both of your legs into the chest. Relax your neck and shoulders. Hold for 10-20 seconds and then switch sides.	2
6769	80	Run a band around a stationary post like that of a squat rack.	0
6770	80	Grab the band by the handles and stand back so that the tension in the band rises.	1
6771	80	Extend and lift the arms straight in front of you. Tip: Your arms should be straight and parallel to the floor while perpendicular to your torso. Your feet should be firmly planted on the floor spread at shoulder width. This will be your starting position.	2
6772	80	As you exhale, move your arms to the sides and back. Keep your arms extended and parallel to the floor. Continue the movement until the arms are extended to your sides.	3
6773	80	After a pause, go back to the original position as you inhale.	4
6774	80	Repeat for the recommended amount of repetitions.	5
6775	81	Load a sled with the desired weight, attaching a rope or straps to the sled that you can hold onto.	0
6776	81	Begin the exercise by moving backwards for a given distance. Leaning back, extend through the legs for short steps to move as quickly as possible.	1
6780	83	Secure a band to the base of a rack or the bench. Lay on the bench so that the band is lined up with your head.	0
6781	83	Take hold of the band, raising your elbows so that the upper arm is perpendicular to the floor. With the elbow flexed, the band should be above your head. This will be your starting position.	1
6782	83	Extend through the elbow to straighten your arm, keeping your upper arm in place. Pause at the top of the motion, and return to the starting position.	2
6783	84	Hold the dumbbells and lay down on a flat bench in such a way that around 1/4 of your head is over the edge.	0
6784	84	Stretch your arms with the weights and bend them so that the dumbbells are lowered (make sure they don't touch each other).	1
6785	84	Just before they touch your forehead, push them up.	2
6786	84	Pay attention to your elbows and arms: only the triceps are doing the work, the rest of the arms should not move	3
6787	85	Begin seated on the ground with a loaded barbell over your legs. Using a fat bar or having a pad on the bar can greatly reduce the discomfort caused by this exercise. Roll the bar so that it is directly above your hips, and lay down flat on the floor.	0
6790	86	Stand up straight with your feet at shoulder width as you hold a barbell with both hands in front of you using a pronated grip (palms facing the thighs). Tip: Your hands should be a little wider than shoulder width apart. You can use wrist wraps for this exercise for a better grip. This will be your starting position.	0
6791	86	Raise your shoulders up as far as you can go as you breathe out and hold the contraction for a second. Tip: Refrain from trying to lift the barbell by using your biceps.	1
6792	86	Slowly return to the starting position as you breathe in.	2
6793	86	Repeat for the recommended amount of repetitions.	3
6794	87	Stand up straight while holding a barbell placed on the back of your shoulders (slightly below the neck) and stand upright behind an elevated platform (such as the one used for spotting behind a flat bench). This is your starting position.	0
6795	87	Place the right foot on the elevated platform. Step on the platform by extending the hip and the knee of your right leg. Use the heel mainly to lift the rest of your body up and place the foot of the left leg on the platform as well. Breathe out as you execute the force required to come up.	1
6796	87	Step down with the left leg by flexing the hip and knee of the right leg as you inhale. Return to the original standing position by placing the right foot of to next to the left foot on the initial position.	2
6797	87	Repeat with the right leg for the recommended amount of repetitions and then perform with the left leg.	3
6798	88	For this exercise you will need a heavy rope anchored at its center 15-20 feet away. Standing in front of the rope, take an end in each hand with your arms extended at your side. This will be your starting position.	0
6799	88	Initiate the movement by rapidly raising one arm to shoulder level as quickly as you can.	1
6800	88	As you let that arm drop to the starting position, raise the opposite side.	2
6801	88	Continue alternating your left and right arms, whipping the ropes up and down as fast as you can.	3
6802	89	Wearing either a harness or a loose weight belt, attach the chain to the back so that you will be facing away from the sled. Bend down so that your hands are on the ground. Your back should be flat and knees bent. This is your starting position.	0
6803	89	Begin by driving with legs, alternating left and right. Use your hands to maintain balance and to help pull. Try to keep your back flat as you move over a given distance.	1
6804	90	Lie on a flat bench with a barbell using a shoulder grip width.	0
6805	90	Hold the bar straight over your chest with a bend in your arms. This will be your starting position.	1
6806	90	While keeping your arms in the bent arm position, lower the weight slowly in an arc behind your head while breathing in until you feel a stretch on the chest.	2
6807	90	At that point, bring the barbell back to the starting position using the arc through which the weight was lowered and exhale as you perform this movement.	3
6808	90	Hold the weight on the initial position for a second and repeat the motion for the prescribed number of repetitions.	4
6809	97	Initiate the exercise by standing upright with a kettlebell in one hand.	0
6810	97	Swing the kettlebell back forcefully and then reverse the motion forcefully. Crush the kettlebell handle as hard as possible and raise the kettlebell to your shoulder.	1
6811	95	Position two equally loaded EZ bars on the ground next to each other. Ensure they are able to roll.	0
6812	95	Assume a push-up position over the bars, supporting your weight on your toes and hands with your arms extended and body straight.	1
6813	95	Place your hands on the bars. This will be your starting position.	2
6814	95	Using a slow and controlled motion, move your hands away from the midline of your body, rolling the bars apart. Inhale during this portion of the motion.	3
6815	95	After moving the bars as far apart as you can, return to the starting position by pulling them back together. Exhale as you perform this movement.	4
6816	96	Connect a standard handle to each arm of a cable machine, and position them in the most downward position.	0
6817	96	Grab a Bosu Ball and position it in front and center of the cable machine.	1
6818	96	Lie down on the Bosu Ball with the small of your back arched around the ball. Your rear end should be close to the floor without touching it.	2
6819	96	With both hands, reach back and grab the handle of each cable.	3
6820	96	With your feet positioned in a wide stance, extend your arms straight out in front of you and in between your knees. Your hands should be at knee level.	4
6821	96	Keep your arms straight and in-line with the upward angle of the cable. Elevate your torso in a crunching motion without dropping or bending your arms.	5
6822	96	Maintain the rigid position with your arms. Slowly descend back to the starting position with your back arched around the Bosu Ball and your abdominals elongated.	6
6823	96	Repeat the same series of movements to failure.	7
6824	96	Once you reach failure, keep your abs tight and raise your torso into plank position so your back is elevated off the Bosu Ball.	8
6825	96	Lower your arms down to your side; keep them straight. Start doing alternating side bends; reach for your heels! This finishing movement will focus on your obliques.	9
6826	99	Sit on a Military Press Bench with a bar at shoulder level with a pronated grip (palms facing forward). Tip: Your grip should be wider than shoulder width and it should create a 90-degree angle between the forearm and the upper arm as the barbell goes down. This is your starting position.	0
6827	99	Once you pick up the barbell with the correct grip, lift the bar up over your head by locking your arms.	1
6828	99	Now lower the bar down to the back of the head slowly as you inhale.	2
6829	99	Lift the bar back up to the starting position as you exhale.	3
6830	99	Lower the bar down to the starting position slowly as you inhale. This is one repetition.	4
6831	99	Alternate in this manner until you complete the recommended amount of repetitions.	5
6832	98	Lie on your side, with your upper arm against the foam roller. The upper arm should be more or less aligned with your body, with the outside of the bicep pressed against the foam roller.	0
6833	98	Raise your hips off of the floor, supporting your weight on your arm and on your feet. Hold for 10-30 seconds, and then switch sides.	1
6834	93	To begin, seat yourself on the bike and adjust the seat to your height.	0
6835	94	To begin, seat yourself on the bike and adjust the seat to your height.	0
6836	94	Select the desired option from the menu. You may have to start pedaling to turn it on. You can use the manual setting, or you can select a program to use. Typically, you can enter your age and weight to estimate the amount of calories burned during exercise. The level of resistance can be changed throughout the workout. The handles can be used to monitor your heart rate to help you stay at an appropriate intensity.	1
6837	225	Lie facedown on the floor.	0
6838	225	Put your left hand under your left hipbone to pad your hip and pubic bone.	1
6839	225	Bend your right knee so you can hold the foot in your right hand.	2
6840	225	Lift the foot in the air and simultaneously lift your shoulders off the floor. This also stretches the right hip flexor and the chest and shoulders. Switch sides. If it doesn't bother your back, you can try it with both arms and legs at the same time.	3
6841	102	To get yourself into the starting position, place the pulleys on a high position (above your head), select the resistance to be used and hold the pulleys in each hand.	0
6842	102	Step forward in front of an imaginary straight line between both pulleys while pulling your arms together in front of you. Your torso should have a small forward bend from the waist. This will be your starting position.	1
6843	102	With a slight bend on your elbows in order to prevent stress at the biceps tendon, extend your arms to the side (straight out at both sides) in a wide arc until you feel a stretch on your chest. Breathe in as you perform this portion of the movement. Tip: Keep in mind that throughout the movement, the arms and torso should remain stationary; the movement should only occur at the shoulder joint.	2
6844	102	Return your arms back to the starting position as you breathe out. Make sure to use the same arc of motion used to lower the weights.	3
6845	102	Hold for a second at the starting position and repeat the movement for the prescribed amount of repetitions.	4
6846	105	Lie on incline an bench facing away from a high pulley machine that has a straight bar attachment on it.	0
6847	105	Grasp the straight bar attachment overhead with a pronated (overhand; palms down) shoulder width grip and extend your arms in front of you. The bar should be around 2 inches away from your upper thighs. This will be your starting position.	1
6848	105	Keeping the upper arms stationary, lift your arms back in a semi circle until the bar is straight over your head. Breathe in during this portion of the movement.	2
6849	105	Slowly go back to the starting position using your lats and hold the contraction once you reach the starting position. Breathe out during the execution of this movement.	3
6850	105	Repeat for the recommended amount of repetitions.	4
6851	106	Begin by moving the pulleys to the high position, select the resistance to be used, and take a handle in each hand.	0
6852	106	Stand directly between both pulleys with your arms extended out to your sides. Your head and chest should be up while your arms form a . This will be your starting position.	1
6853	106	Keeping the elbows extended, pull your arms straight to your sides.	2
6854	106	Return your arms back to the starting position after a pause at the peak contraction.	3
6855	106	Continue the movement for the prescribed number of repetitions.	4
6856	107	Connect a rope attachment to a tower, and move the cable to the lowest pulley position. Stand with your side to the cable with a wide stance, and grab the rope with both hands.	0
6857	107	Twist your body away from the pulley as you bring the rope over your shoulder like you performing a judo flip.	1
6858	107	Shift your weight between your feet as you twist and crunch forward, pulling the cable downward.	2
6859	107	Return to the starting position and repeat until failure.	3
6860	107	Then, reposition and repeat the same series of movements on the opposite side.	4
6861	108	Adjust the pulleys to the appropriate height and adjust the weight. The pulleys should be above your head.	0
6862	108	Grab the left pulley with your right hand and the right pulley with your left hand, crossing them in front of you. This will be your starting position.	1
6863	108	Initiate the movement by moving your arms back and outward, keeping your arms straight as you execute the movement.	2
6864	108	Pause at the end of the motion before returning the handles to the start position.	3
6865	110	Sit in the same position on a low pulley row station as you would if you were doing seated cable rows for the back.	0
6866	110	Attach a rope to the pulley and grasp it with an overhand grip. Your arms should be extended and parallel to the floor with the elbows flared out.	1
6867	110	Keep your lower back upright and slide your hips back so that your knees are slightly bent. This will be your starting position.	2
6868	110	Pull the cable attachment towards your upper chest, just below the neck, as you keep your elbows up and out to the sides. Continue this motion as you exhale until the elbows travel slightly behind the back. Tip: Keep your upper arms horizontal, perpendicular to the torso and parallel to the floor throughout the motion.	3
6869	110	Go back to the initial position where the arms are extended and the shoulders are stretched forward. Inhale as you perform this portion of the movement.	4
6870	110	Repeat for the recommended amount of repetitions.	5
6871	111	Connect a standard handle attachment, and position the cable to a middle pulley position.	0
6872	111	Lie on a stability ball perpendicular to the cable and grab the handle with one hand. You should be approximately arm length away from the pulley, with the tension of the weight on the cable.	1
6873	111	Grab the handle with both hands and fully extend your arms above your chest. You hands should be directly in-line with the pulley. If not, adjust the pulley up or down until they are.	2
6874	111	Keep your hips elevated and abs engaged. Rotate your torso away from the pulley for a full-quarter rotation. Your body should be flat from head to knees.	3
6875	111	Pause for a moment and in a slow and controlled manner reset to the starting position. You should still have side tension on the cable in the resting position.	4
6876	111	Repeat the same movement to failure.	5
6877	111	Then, reposition and repeat the same series of movements on the opposite side.	6
6878	112	Seat on a flat bench with your back facing a high pulley.	0
7005	151	Perform the motion by flexing the spine and rotating your torso to bring the left elbow to the right knee.	1
6879	112	Grasp the cable rope attachment with both hands (with the palms of the hands facing each other) and place your hands securely over both shoulders. Tip: Allow the weight to hyperextend the lower back slightly. This will be your starting position.	1
6880	112	With the hips stationary, flex the waist so the elbows travel toward the hips. Breathe out as you perform this step.	2
6881	112	As you inhale, go back to the initial position slowly.	3
6882	112	Repeat for the recommended amount of repetitions.	4
6883	113	Grasp a cable bar attachment that is attached to a low pulley with a shoulder width or slightly wider overhand (palms facing down) grip.	0
6884	113	Stand erect close to the pulley with your arms extended in front of you holding the bar. This will be your starting position.	1
6885	113	Lift the bar by elevating the shoulders as high as possible as you exhale. Hold the contraction at the top for a second. Tip: The arms should remain extended at all times. Refrain from using the biceps to help lift the bar. Only the shoulders should be moving up and down.	2
6886	113	Lower the bar back to the original position.	3
6887	113	Repeat for the recommended amount of repetitions.	4
6891	116	Begin seated on the floor. Place a foam roller underneath your lower leg. Your other leg can either be crossed over the opposite or be placed on the floor, supporting some of your weight. This will be your starting position.	0
6892	116	Place your hands to your side or just behind you, and press down to raise your hips off of the floor, placing much of your weight against your calf muscle. Roll from below the knee to above the ankle, pausing at points of tension for 10-30 seconds. Repeat for the other leg.	1
6893	117	While standing upright, hold a barbell plate in both hands at the 3 and 9 o'clock positions. Your palms should be facing each other and your arms should be extended straight out in front of you. This will be your starting position.	0
6894	117	Initiate the movement by rotating the plate as far to one side as possible. Use the same type of movement you would use to turn a steering wheel to one side.	1
6895	117	Reverse the motion, turning it all the way to the opposite side.	2
6896	117	Repeat for the recommended amount of repetitions.	3
6897	118	Begin with your feet a few inches apart and your left arm up in a relaxed, athletic position.	0
6898	118	With your right foot, quick step behind and pull the knee up.	1
6899	118	Fire your arms back up when you pull the right knee, being sure that your knee goes straight up and down. Avoid turning your feet as you move and continue to look forward as you move to the side.	2
6900	119	Begin standing while facing a wall or a partner.	0
6901	119	Using both hands, position the ball behind your head, stretching as much as possible, and forcefully throw the ball forward.	1
6902	119	Ensure that you follow your throw through, being prepared to receive your rebound from your throw. If you are throwing against the wall, make sure that you stand close enough to the wall to receive the rebound, and aim a little higher than you would with a partner.	2
6903	121	Begin in a three point stance, squatted down with your back flat and one hand on the ground. Place the medicine ball directly in front of you.	0
6904	121	To begin, take your first step as you pull the ball to your chest, positioning both hands to prepare for the throw.	1
6905	121	As you execute the second step, explosively release the ball forward as hard as possible.	2
6906	124	The circus bell is an oversized dumbbell with a thick handle. Begin with the dumbbell between your feet, and grip the handle with both hands.	0
6907	124	Clean the dumbbell by extending through your hips and knees to deliver the implement to the desired shoulder, letting go with the extra hand.	1
6908	124	Ensure that you get one of the dumbbell heads behind the shoulder to keep from being thrown off balance. To raise it overhead, dip by flexing the knees, and the drive upwards as you extend the dumbbell overhead, leaning slightly away from it as you do so.	2
6909	124	Carefully guide the bell back to the floor, keeping it under control as much as possible. It is best to perform this event on a thick rubber mat to prevent damage to the floor.	3
6910	125	Lie on a flat bench with an EZ bar loaded to an appropriate weight.	0
6911	125	Using a narrow grip lift the bar and hold it straight over your torso with your elbows in. The arms should be perpendicular to the floor. This will be your starting position.	1
6912	125	Now lower the bar down to your lower chest as you breathe in. Keep the elbows in as you perform this movement.	2
6913	125	Using the triceps to push the bar back up, press it back to the starting position by extending the elbows as you exhale.	3
6914	125	Repeat.	4
6915	128	Lie flat on your back and bend your knees about 60 degrees.	0
6916	128	Keep your feet flat on the floor and place your hands loosely behind your head. This will be your starting position.	1
6917	128	Now curl up and bring your right elbow and shoulder across your body while bring your left knee in toward your left shoulder at the same time. Reach with your elbow and try to touch your knee. Exhale as you perform this movement. Tip: Try to bring your shoulder up towards your knee rather than just your elbow and remember that the key is to contract the abs as you perform the movement; not just to move the elbow.	2
6918	128	Now go back down to the starting position as you inhale and repeat with the left elbow and the right knee.	3
6919	128	Continue alternating in this manner until all prescribed repetitions are done.	4
6920	120	Start off by standing with your legs together, holding a bodybar or a broomstick.	0
6921	120	Take a slightly wider than shoulder width grip on the pole and hold it in front of you with your palms facing down.	1
6922	120	Carefully lift the pole up and behind your head.	2
6923	122	Get on your hands and knees next to an exercise ball.	0
6924	122	Place your elbows on top of the ball, keeping your arm out to your side. This will be your starting position.	1
6925	122	Lower your torso towards the floor, keeping your elbow on top of the ball. Hold the stretch for 20-30 seconds, and repeat with the other arm.	2
6926	130	In the crucifix, you statically hold weights out to the side for time. While the event can be practiced using dumbbells, it is best to practice with one of the various implements used, such as axes and hammers, as it feels different.	0
6927	130	Begin standing, and raise your arms out to the side holding the implements. Your arms should be parallel to the ground. In competition, judges or sensors are used to let you know when you break parallel. Hold for as long as you can. Typically, the weights should be heavy enough that you fail in 30-60 seconds.	1
6928	131	Lie on the floor with your back flat and knees bent with around a 60-degree angle between the hamstrings and the calves.	0
6929	131	Keep your feet flat on the floor and stretch your arms overhead with your palms crossed. This will be your starting position.	1
6930	131	Curl your upper body forward and bring your shoulder blades just off the floor. At all times, keep your arms aligned with your head, neck and shoulder. Don't move them forward from that position. Exhale as you perform this portion of the movement and hold the contraction for a second.	2
6931	131	Slowly lower down to the starting position as you inhale.	3
6932	131	Repeat for the recommended amount of repetitions.	4
6939	134	Secure your legs at the end of the decline bench and lie down.	0
6940	134	Now place your hands lightly on either side of your head keeping your elbows in. Tip: Don't lock your fingers behind your head.	1
6941	134	While pushing the small of your back down in the bench to better isolate your abdominal muscles, begin to roll your shoulders off it.	2
6942	134	Continue to push down as hard as you can with your lower back as you contract your abdominals and exhale. Your shoulders should come up off the bench only about four inches, and your lower back should remain on the bench. At the top of the movement, contract your abdominals hard and keep the contraction for a second. Tip: Focus on slow, controlled movement - don't cheat yourself by using momentum.	3
6943	134	After the one second contraction, begin to come down slowly again to the starting position as you inhale.	4
6944	134	Repeat for the recommended amount of repetitions.	5
6945	135	Secure your legs at the end of the decline bench and lie down with a dumbbell on each hand on top of your thighs. The palms of your hand will be facing each other.	0
6946	135	Once you are laying down, move the dumbbells in front of you at shoulder width. The palms of the hands should be facing each other and the arms should be perpendicular to the floor and fully extended. This will be your starting position.	1
7469	291	With your feet positioned shoulder width apart, reach upward with your other hand and grab the handle with both hands. Your arms should still be fully extended.	2
6947	135	With a slight bend on your elbows in order to prevent stress at the biceps tendon, lower your arms out at both sides in a wide arc until you feel a stretch on your chest. Breathe in as you perform this portion of the movement. Tip: Keep in mind that throughout the movement, the arms should remain stationary; the movement should only occur at the shoulder joint.	2
6948	135	Return your arms back to the starting position as you squeeze your chest muscles and breathe out. Tip: Make sure to use the same arc of motion used to lower the weights.	3
6949	135	Hold for a second at the contracted position and repeat the movement for the prescribed amount of repetitions.	4
6950	136	Secure your legs at the end of the decline bench and slowly lay down on the bench.	0
6951	136	Raise your upper body off the bench until your torso is about 35-45 degrees if measured from the floor.	1
6952	136	Put one hand beside your head and the other on your thigh. This will be your starting position.	2
6953	136	Raise your upper body slowly from the starting position while turning your torso to the left. Continue crunching up as you exhale until your right elbow touches your left knee. Hold this contracted position for a second. Tip: Focus on keeping your abs tight and keeping the movement slow and controlled.	3
6954	136	Lower your body back down slowly to the starting position as you inhale.	4
6955	136	After completing one set on the right for the recommended amount of repetitions, switch to your left side. Tip: Focus on really twisting your torso and feeling the contraction when you are in the up position.	5
6956	137	Lie on your back on a decline bench and hold on to the top of the bench with both hands. Don't let your body slip down from this position.	0
6957	137	Hold your legs parallel to the floor using your abs to hold them there while keeping your knees and feet together. Tip: Your legs should be fully extended with a slight bend on the knee. This will be your starting position.	1
6958	137	While exhaling, move your legs towards the torso as you roll your pelvis backwards and you raise your hips off the bench. At the end of this movement your knees will be touching your chest.	2
6959	137	Hold the contraction for a second and move your legs back to the starting position while inhaling.	3
6960	137	Repeat for the recommended amount of repetitions.	4
6961	138	Sit securely in a dip machine, select the weight and firmly grasp the handles.	0
6962	138	Now keep your elbows in at your sides in order to place emphasis on the triceps. The elbows should be bent at a 90 degree angle.	1
6963	138	As you contract the triceps, extend your arms downwards as you exhale. Tip: At the bottom of the movement, focus on keeping a little bend in your arms to keep tension on the triceps muscle.	2
6964	138	Now slowly let your arms come back up to the starting position as you inhale.	3
6965	138	Repeat for the recommended amount of repetitions.	4
6966	141	Place a kettlebell in front of your front foot and clean and press a kettlebell overhead with your opposite arm. Clean the kettlebell to your shoulder by extending through the legs and hips as you pull the kettlebell towards your shoulders. Rotate your wrist as you do so, so that the palm faces forward.	0
6967	141	Keeping the kettlebell locked out at all times, push your butt out in the direction of the locked out kettlebell. Turn your feet out at a forty-five degree angle from the arm with the locked out kettlebell.	1
6968	141	Bending at the hip to one side, sticking your butt out, slowly lean until you can retrieve the kettlebell from the floor. Keep your eyes on the kettlebell that you hold over your head at all times.	2
6969	141	Pause for a second after retrieving the kettlebell from the ground and reverse the motion back to the starting position.	3
6970	142	Lie facedown on top of an exercise ball.	0
6971	142	While resting on your stomach on the ball, walk your hands forward along the floor and lift your legs, extending your elbows and knees.	1
6972	143	Lie down on a flat bench with a dumbbell on each hand resting on top of your thighs. The palms of your hand will be facing each other.	0
6973	143	Then using your thighs to help raise the dumbbells, lift the dumbbells one at a time so you can hold them in front of you at shoulder width with the palms of your hands facing each other. Raise the dumbbells up like you're pressing them, but stop and hold just before you lock out. This will be your starting position.	1
6974	143	With a slight bend on your elbows in order to prevent stress at the biceps tendon, lower your arms out at both sides in a wide arc until you feel a stretch on your chest. Breathe in as you perform this portion of the movement. Tip: Keep in mind that throughout the movement, the arms should remain stationary; the movement should only occur at the shoulder joint.	2
6975	143	Return your arms back to the starting position as you squeeze your chest muscles and breathe out. Tip: Make sure to use the same arc of motion used to lower the weights.	3
6976	143	Hold for a second at the contracted position and repeat the movement for the prescribed amount of repetitions.	4
6977	144	Lie on a flat bench face down with one arm holding a dumbbell and the other hand on top of the bench folded so that you can rest your head on it.	0
6978	144	Bend the elbows of the arm holding the dumbbell so that it creates a 90-degree angle between the upper arm and the forearm.	1
6979	144	Now raise the upper arm so that the forearm is perpendicular to the floor and the upper arm is perpendicular to your torso. Tip: The upper arm should be parallel to the floor and also creating a 90-degree angle with your torso. This will be your starting position.	2
6980	144	As you breathe out, externally rotate your forearm so that the dumbbell is lifted forward as you maintain the 90 degree angle bend between the upper arms and the forearm. You will continue this external rotation until the forearm is parallel to the floor. At this point you will hold the contraction for a second.	3
6981	144	As you breathe in, slowly go back to the starting position.	4
6982	144	Repeat for the recommended amount of repetitions.	5
6983	145	Lie sideways on a flat bench with one arm holding a dumbbell and the other hand on top of the bench folded so that you can rest your head on it.	0
6984	145	Bend the elbows of the arm holding the dumbbell so that it creates a 90-degree angle between the upper arm and the forearm.	1
6985	145	Now raise the upper arm so that the forearm is parallel to the floor and perpendicular to your torso (Tip: So the forearm will be directly in front of you). The upper arm will be stationary by your torso and should be parallel to the floor (aligned with your torso at all times). This will be your starting position.	2
6986	145	As you breathe out, externally rotate your forearm so that the dumbbell is lifted up in a semicircle motion as you maintain the 90 degree angle bend between the upper arms and the forearm. You will continue this external rotation until the forearm is perpendicular to the floor and the torso pointing towards the ceiling. At this point you will hold the contraction for a second.	3
6987	145	As you breathe in, slowly go back to the starting position.	4
6988	145	Repeat for the recommended amount of repetitions and then switch to the other arm.	5
6989	146	This corrective exercise strengthens the muscles that stabilize your shoulder blade. Hold a light weight in each hand, hanging at your sides. Your thumbs should pointing up.	0
6990	146	Begin the movement raising your arms out in front of you, about 30 degrees off center. Your arms should be fully extended as you perform the movement.	1
6991	146	Continue until your arms are parallel to the ground, and then return to the starting position.	2
6992	147	Stand erect with a dumbbell on each hand (palms facing your torso), arms extended on the sides.	0
6993	147	Lift the dumbbells by elevating the shoulders as high as possible while you exhale. Hold the contraction at the top for a second. Tip: The arms should remain extended at all times. Refrain from using the biceps to help lift the dumbbells. Only the shoulders should be moving up and down.	1
6994	147	Lower the dumbbells back to the original position.	2
6995	147	Repeat for the recommended amount of repetitions.	3
6996	148	Stand up straight while holding a dumbbell on each hand (palms facing the side of your legs).	0
6997	148	Place the right foot on the elevated platform. Step on the platform by extending the hip and the knee of your right leg. Use the heel mainly to lift the rest of your body up and place the foot of the left leg on the platform as well. Breathe out as you execute the force required to come up.	1
6998	148	Step down with the left leg by flexing the hip and knee of the right leg as you inhale. Return to the original standing position by placing the right foot of to next to the left foot on the initial position.	2
6999	148	Repeat with the right leg for the recommended amount of repetitions and then perform with the left leg.	3
7000	149	Using a close grip, lift the EZ bar and hold it with your elbows in as you lie on the bench. Your arms should be perpendicular to the floor. This will be your starting position.	0
7001	149	Keeping the upper arms stationary, lower the bar by allowing the elbows to flex. Inhale as you perform this portion of the movement. Pause once the bar is directly above the forehead.	1
7002	149	Lift the bar back to the starting position by extending the elbow and exhaling.	2
7003	149	Repeat.	3
7004	151	Lie on the floor, crossing your right leg across your bent left knee. Clasp your hands behind your head, beginning with your shoulder blades on the ground. This will be your starting position.	0
7006	151	Return to the starting position and repeat the movement for the desired number of repetitions before switching sides.	2
7007	150	Sit or stand with your feet slightly apart.	0
7008	150	Place your hands on your shoulders with your elbows at shoulder level and pointing out.	1
7009	150	Slowly make a circle with your elbows. Breathe out as you start the circle and breathe in as you complete the circle.	2
7010	153	Lie on the floor and position a kettlebell for one arm to press. The kettlebell should be held by the handle. The leg on the same side that you are pressing should be bent, with the knee crossing over the midline of the body.	0
7011	153	Press the kettlebell by extending the elbow and adducting the arm, pressing it above your body. Return to the starting position.	1
7012	226	Grab onto a chinup bar with one hand, using a pronated grip. Keep your feet on the floor or a step. Allow the majority of your weight to hang from that hand, while keeping your feet on the ground. Hold for 10-20 seconds and switch sides.	0
7013	154	Start in a relaxed position with one leg slightly forward. This will be your starting position.	0
7015	154	Perform fast skips by maintaining close contact with the ground and reduce air time, moving as quickly as possible.	2
7016	155	Hold a barbell with both hands and your palms facing up; hands spaced about shoulder width.	0
7017	155	Place your feet flat on the floor, at a distance that is slightly wider than shoulder width apart. This will be your starting position.	1
7018	155	Lower the bar as far as possible by extending the fingers. Allowing the bar to roll down the hands, catch the bar with the final joint in the fingers.	2
7019	155	Now curl bar up as high as possible by closing your hands while exhaling. Hold the contraction at the top.	3
7022	156	On a flat bench lie facedown with the hips on the edge of the bench, the legs straight with toes high off the floor and with the arms on top of the bench holding on to the front edge.	0
7023	156	Squeeze your glutes and hamstrings and straighten the legs until they are level with the hips. This will be your starting position.	1
7024	156	Start the movement by lifting the left leg higher than the right leg.	2
7025	156	Then lower the left leg as you lift the right leg.	3
7026	156	Continue alternating in this manner (as though you are doing a flutter kick in water) until you have done the recommended amount of repetitions for each leg. Make sure that you keep a controlled movement at all times. Tip: You will breathe normally as you perform this movement.	4
7027	158	Stand with your hands behind your head, and squat down keeping your torso upright and your head up. This will be your starting position.	0
7028	158	Jump forward several feet, avoiding jumping unnecessarily high. As your feet contact the ground, absorb the impact through your legs, and jump again. Repeat this action 5-10 times.	1
7029	159	Grasp the pull-up bar with a shoulder width underhand grip.	0
7030	159	Now hang with your arms fully extended and stick your chest out and lean back. Tip: You will be leaning back throughout the entire movement. This will be your starting position.	1
7031	159	Start pulling yourself towards the bar with your spine arched throughout the movement and your head leaning back as far away from the bar as possible. Exhale as you perform this portion of the movement. Tip: At the upper end of the movement, your hips and legs will be at about a 45-degree angle to the floor.	2
7032	159	Keep pulling until your collarbone passes the bar and your lower chest or sternum area touches it. Hold that contraction for a second. Tip: By the time you've completed this portion of the movement; your head will be parallel to the floor.	3
7035	160	Kneel on the floor or an exercise mat and bend at the waist with your arms extended in front of you (perpendicular to the torso) in order to get into a kneeling push-up position but with the arms spaced at shoulder width. Your head should be looking forward and the bend of the knees should create a 90-degree angle between the hamstrings and the calves. This will be your starting position.	0
7036	160	As you exhale, lift up your right leg until the hamstrings are in line with the back while maintaining the 90-degree angle bend. Contract the glutes throughout this movement and hold the contraction at the top for a second. Tip: At the end of the movement the upper leg should be parallel to the floor while the calf should be perpendicular to it.	1
7037	160	Go back to the initial position as you inhale and now repeat with the left leg.	2
7038	160	Continue to alternate legs until all of the recommended repetitions have been performed.	3
7039	161	Hang from a chin-up bar using an underhand grip (palms facing you) that is slightly wider than shoulder width.	0
7040	161	Now bend your knees at a 90 degree angle so that the calves are parallel to the floor while the thighs remain perpendicular to it. This will be your starting position.	1
7041	161	As you exhale, pull yourself up while crunching your knees up at the same time until your knees are at chest level. You will stop going up as soon as your nose is at the same level as the bar. Tip: When you get to this point you should also be finishing the crunch at the same time.	2
7042	161	Slowly start to inhale as you return to the starting position.	3
7043	161	Repeat for the recommended amount of repetitions.	4
7044	162	Begin in a pushup position on the floor. This will be your starting position.	0
7045	162	Using both legs, jump forward landing with your feet next to your hands. Keep your head up as you do so.	1
7046	162	Return to the starting position and immediately repeat the movement, continuing for 10-20 repetitions.	2
7050	165	Seat yourself on the floor.	0
7051	165	Straddle an exercise ball between both legs and lower your hips down toward the floor.	1
7052	165	Hug your arms around the ball to support your body. Adjust your legs so that your feet are flat on the floor and your knees line up over your ankles. Keep a good grip on the ball so it doesn't roll away from you and send you back onto your buttocks.	2
7053	166	Lie down on your back and pull both knees up to your chest.	0
7054	166	Hold your arms under the knees, not over (that would put to much pressure on your knee joints).	1
7055	166	Slowly pull the knees toward your shoulders. This also stretches your buttocks muscles.	2
7056	164	Secure one end of the band to the lower portion of a post and attach the other to one ankle.	0
7057	164	Face away from the attachment point of the band.	1
7058	164	Keeping your head and your chest up, raise your knee up to 90 degrees and pause.	2
7047	672	In a seated position, extend your legs over a foam roll so that it is position on the back of the upper legs. Place your hands to the side or behind you to help support your weight. This will be your starting position.	0
7048	672	Using your hands, lift your hips off of the floor and shift your weight on the foam roll to one leg. Relax the hamstrings of the leg you are stretching.	1
7059	164	Return the leg to the starting position.	3
7060	167	Set up a row of hurdles or other small barriers, placing them a few feet apart.	0
7061	167	Stand in front of the first hurdle with your feet shoulder width apart. This will be your starting position.	1
7062	167	Begin by jumping with both feet over the first hurdle, swinging both arms as you jump.	2
7063	167	Absorb the impact of landing by bending the knees, rebounding out of the first leap by jumping over the next hurdle. Continue until you have jumped over all of the hurdles.	3
7064	223	Pick a dumbbell and place it in one of your hands. Your non lifting hand should be used to grab something steady such as an incline bench press. Lean towards your lifting arm and away from the hand that is gripping the incline bench as this will allow you to keep your balance.	0
7065	223	Stand with a straight torso and have the dumbbell by your side at arm length with the palm of the hand facing you. This will be your starting position.	1
7066	223	While maintaining the torso stationary (no swinging), lift the dumbbell to your side with a slight bend on the elbow and your hand slightly tilted forward as if pouring water in a glass. Continue to go up until you arm is parallel to the floor. Exhale as you execute this movement and pause for a second at the top.	2
7067	223	Lower the dumbbell back down slowly to the starting position as you inhale.	3
7068	223	Repeat for the recommended amount of repetitions.	4
7069	223	Switch arms and repeat the exercise.	5
7070	168	Lie face down on a hyperextension bench, tucking your ankles securely under the footpads.	0
7071	168	Adjust the upper pad if possible so your upper thighs lie flat across the wide pad, leaving enough room for you to bend at the waist without any restriction.	1
7072	168	With your body straight, cross your arms in front of you (my preference) or behind your head. This will be your starting position. Tip: You can also hold a weight plate for extra resistance in front of you under your crossed arms.	2
7073	168	Start bending forward slowly at the waist as far as you can while keeping your back flat. Inhale as you perform this movement. Keep moving forward until you feel a nice stretch on the hamstrings and you can no longer keep going without a rounding of the back. Tip: Never round the back as you perform this exercise. Also, some people can go farther than others. The key thing is that you go as far as your body allows you to without rounding the back.	3
7074	168	Slowly raise your torso back to the initial position as you inhale. Tip: Avoid the temptation to arch your back past a straight line. Also, do not swing the torso at any time in order to protect the back from injury.	4
7075	168	Repeat for the recommended amount of repetitions.	5
7076	170	Lay on your side, with the bottom leg placed onto a foam roller between the hip and the knee. The other leg can be crossed in front of you.	0
7077	170	Place as much of your weight as is tolerable onto your bottom leg; there is no need to keep your bottom leg in contact with the ground. Be sure to relax the muscles of the leg you are stretching.	1
7078	170	Roll your leg over the foam from you hip to your knee, pausing for 10-30 seconds at points of tension. Repeat with the opposite leg.	2
7079	171	Stand with your feet close together. Keeping your legs straight, stretch down and put your hands on the floor directly in front of you. This will be your starting position.	0
7080	171	Begin by walking your hands forward slowly, alternating your left and your right. As you do so, bend only at the hip, keeping your legs straight.	1
7081	171	Keep going until your body is parallel to the ground in a pushup position.	2
7082	171	Now, keep your hands in place and slowly take short steps with your feet, moving only a few inches at a time.	3
7083	171	Continue walking until your feet are by hour hands, keeping your legs straight as you do so.	4
7084	172	To get yourself into the starting position, set the pulleys at the floor level (lowest level possible on the machine that is below your torso).	0
7085	172	Place an incline bench (set at 45 degrees) in between the pulleys, select a weight on each one and grab a pulley on each hand.	1
7086	172	With a handle on each hand, lie on the incline bench and bring your hands together at arms length in front of your face. This will be your starting position.	2
7087	172	With a slight bend of your elbows (in order to prevent stress at the biceps tendon), lower your arms out at both sides in a wide arc until you feel a stretch on your chest. Breathe in as you perform this portion of the movement. Tip: Keep in mind that throughout the movement, the arms should remain stationary. The movement should only occur at the shoulder joint.	3
7088	172	Return your arms back to the starting position as you squeeze your chest muscles and exhale. Hold the contracted position for a second. Tip: Make sure to use the same arc of motion used to lower the weights.	4
7089	172	Repeat the movement for the prescribed amount of repetitions.	5
7090	173	Hold a dumbbell on each hand and lie on an incline bench that is set to an incline angle of no more than 30 degrees.	0
7091	173	Extend your arms above you with a slight bend at the elbows.	1
7179	196	Place your right hand onto the line, and thing bring your nose close to your left knee.	1
7092	173	Now rotate the wrists so that the palms of your hands are facing you. Tip: The pinky fingers should be next to each other. This will be your starting position.	2
7093	173	As you breathe in, start to slowly lower the arms to the side while keeping the arms extended and while rotating the wrists until the palms of the hand are facing each other. Tip: At the end of the movement the arms will be by your side with the palms facing the ceiling.	3
7094	173	As you exhale start to bring the dumbbells back up to the starting position by reversing the motion and rotating the hands so that the pinky fingers are next to each other again. Tip: Keep in mind that the movement will only happen at the shoulder joint and at the wrist. There is no motion that happens at the elbow joint.	4
7095	173	Repeat for the recommended amount of repetitions.	5
7096	174	Hold a dumbbell in each hand and lie on an incline bench that is set to an incline angle of no more than 30 degrees.	0
7097	174	Extend your arms above you with a slight bend at the elbows.	1
7098	174	Now rotate the wrists so that the palms of your hands are facing you. Tip: The pinky fingers should be next to each other. This will be your starting position.	2
7439	284	Initiate the movement by shrugging your shoulders straight up. Do not flex the arms or wrist during the movement.	2
7099	174	As you breathe in, start to slowly lower the arms to the side while keeping the arms extended and while rotating the wrists until the palms of the hand are facing each other. Tip: At the end of the movement the arms will be by your side with the palms facing the ceiling.	3
7100	174	As you exhale start to bring the dumbbells back up to the starting position by reversing the motion and rotating the hands so that the pinky fingers are next to each other again. Tip: Keep in mind that the movement will only happen at the shoulder joint and at the wrist. There is no motion that happens at the elbow joint.	4
7101	174	Repeat for the recommended amount of repetitions.	5
7102	177	With your head and neck in a neutral position (normal position with head erect facing forward), place both of your hands on the front side of your head.	0
7103	177	Now gently push forward as you contract the neck muscles but resisting any movement of your head. Start with slow tension and increase slowly. Keep breathing normally as you execute this contraction.	1
7104	177	Hold for the recommended number of seconds.	2
7105	177	Now release the tension slowly.	3
7106	177	Rest for the recommended amount of time and repeat with your hands placed on the back side of your head.	4
7107	178	With your head and neck in a neutral position (normal position with head erect facing forward), place your left hand on the left side of your head.	0
7108	178	Now gently push towards the left as you contract the left neck muscles but resisting any movement of your head. Start with slow tension and increase slowly. Keep breathing normally as you execute this contraction.	1
7109	178	Hold for the recommended number of seconds.	2
7110	178	Now release the tension slowly.	3
7111	178	Rest for the recommended amount of time and repeat with your right hand placed on the right side of your head.	4
7112	179	Assume a push-up position, supporting your weight on your hands and toes while keeping your body straight. Your hands should be just outside of shoulder width. This will be your starting position.	0
7113	179	Begin by shifting your body weight as far to one side as possible, allowing the elbow on that side to flex as you lower your body.	1
7114	179	Reverse the motion by extending the flexed arm, pushing yourself up and then dropping to the other side.	2
7115	179	Repeat for the desired number of repetitions.	3
7116	181	To load kegs, place the desired number a distance from the loading platform, typically 30-50 feet.	0
7117	181	Begin by grabbing the close handle of the first keg, tilting it onto its side to grab the opposite edge of the bottom of the keg. Lift the keg up to your chest.	1
7118	181	The higher you can place the keg, the faster you should be able to move to the platform. Shouldering is usually not allowed. Be sure to keep a firm hold on the keg. Move as quickly as possible to the platform, and load it, extending through your hips, knees, and ankles to get it as high as possible.	2
7119	181	Return to the starting position to retrieve the next keg, and repeat until the event is completed.	3
7470	291	In one motion, pull the handle down and across your body to your front knee while rotating your torso.	3
7120	182	Place one kettlebell between your legs and take a wider than shoulder width stance. Bend over by pushing your butt out and keeping your back flat.	0
7121	182	Pick up a kettlebell and pass it to your other hand between your legs. The receiving hand should reach from behind the legs. Go back and forth for several repetitions.	1
7122	176	Lie face down on the floor, with your arms extended out to your side, palms pressed to the floor. This will be your starting position.	0
7123	176	To begin, flex one knee and bring that leg across the back of your body, attempting to touch it to the ground near the opposite hand.	1
7124	176	Promptly return the leg to the starting postion, and quickly repeat with the other leg. Continue alternating for 10-20 repetitions.	2
7125	183	Place one kettlebell between your legs and take a comfortable stance. Bend over by pushing your butt out and keeping your back flat.	0
7126	183	Pick up a kettlebell and pass it to your other hand between your legs, in the fashion of a W. Go back and forth for several repetitions.	1
7127	187	Lie down on the floor with your right leg straight. Bend your left leg and lower it across your body, holding the knee down toward the floor with your right hand. (The knee doesn't need to touch the floor if you're tight.)	0
7128	187	Place your left arm comfortably beside you and turn your head to the left. Imagine you have a weight tied to your tailbone. let your tailbone fall back toward the floor as your chest reaches in the opposite direction to stretch your lower back. Switch sides.	1
7129	188	Stand with your legs together and hands by your waist.	0
7130	188	Now move your knees in a circular motion as you breathe normally.	1
7131	188	Repeat for the recommended amount of repetitions.	2
7132	184	With a wide stance, hold a kettlebell with both hands. Allow it to hang at waist level with your arms extended. This will be your starting position.	0
7133	184	Initiate the movement by turning to one side, swinging the kettlebell to head height. Briefly pause at the top of the motion.	1
7134	184	Allow the bell to drop as you rotate to the opposite side, again raising the kettlebell to head height.	2
7135	184	Repeat for the desired amount of repetitions.	3
7136	185	Clean two kettlebells to your shoulders. Clean the kettlebells to your shoulders by extending through the legs and hips as you pull the kettlebells towards your shoulders. Rotate your wrists as you do so. This will be your starting position.	0
7137	185	Begin to squat by flexing your hips and knees, lowering your hips between your legs. Maintain an upright, straight back as you descend as low as you can.	1
7138	185	At the bottom, reverse direction and squat by extending your knees and hips, driving through your heels. As you do so, press both kettlebells overhead by extending your arms straight up, using the momentum from the squat to help drive the weights upward.	2
7139	185	As you begin the next repetition, return the weights to the shoulders.	3
7140	186	Place a kettlebell in front of your lead foot and clean and press it overhead with your opposite arm. Clean the kettlebell to your shoulder by extending through the legs and hips as you pull the kettlebell towards your shoulders. Rotate your wrist as you do so, so that the palm faces forward. Press it overhead by extending the elbow.	0
7440	284	After a brief pause return the weight to the starting position.	3
7441	284	Repeat for the desired number of repetitions before engaging the hooks to rack the weight.	4
7141	186	Keeping the kettlebell locked out at all times, push your butt out in the direction of the locked out kettlebell. Turn your feet out at a forty-five degree angle from the arm with the locked out kettlebell. Bending at the hip to one side, sticking your butt out, slowly lean until you can touch the floor with your free hand. Keep your eyes on the kettlebell that you hold over your head at all times.	1
7142	186	Pause for a second after reaching the ground and reverse the motion back to the starting position.	2
7143	189	Position your body on the vertical leg raise bench so that your forearms are resting on the pads next to the torso and holding on to the handles. Your arms will be bent at a 90 degree angle.	0
7144	189	The torso should be straight with the lower back pressed against the pad of the machine and the legs extended pointing towards the floor. This will be your starting position.	1
7145	189	Now as you breathe out, lift your legs up as you keep them extended. Continue this movement until your legs are roughly parallel to the floor and then hold the contraction for a second. Tip: Do not use any momentum or swinging as you perform this exercise.	2
7146	189	Slowly go back to the starting position as you breathe in.	3
7147	189	Repeat for the recommended amount of repetitions.	4
7148	190	This drill helps increase arm efficiency during the run. Begin kneeling, left foot in front, right knee down. Apply pressure through the front heel to keep your glutes and hamstrings activated.	0
7149	190	Begin by blocking the arms in long, pendulum like swings. Close the arm angle, blocking with the arms as you would when jogging, progressing to a run and finally a sprint.	1
7150	190	As soon as your hands pass the hip, accelerate them forward during the sprinting motion to move them as quickly as possible.	2
7151	190	Switch knees and repeat.	3
7152	191	Connect a rope attachment to a high pulley cable and position a mat on the floor in front of it.	0
7153	191	Grab the rope with both hands and kneel approximately two feet back from the tower.	1
7154	191	Position the rope behind your head with your hands by your ears.	2
7155	191	Keep your hands in the same place, contract your abs and pull downward on the rope in a crunching movement until your elbows reach your knees.	3
7156	191	Pause briefly at the bottom and rise up in a slow and controlled manner until you reach the starting position.	4
7157	191	Repeat the same downward movement until you halfway down, at which time you begin rotating one of your elbows to the opposite knee.	5
7158	191	Again, pause briefly at the bottom and rise up in a slow and controlled manner until you reach the starting position.	6
7159	191	Repeat the same movement as before, but alternate the other elbow to the opposite knee.	7
7160	191	Continue this series of movements to failure.	8
7161	192	Position a bar into a landmine or securely anchor it in a corner. Load the bar to an appropriate weight.	0
7474	291	Then, reposition and repeat the same series of movements on the opposite side.	7
7162	192	Raise the bar from the floor, taking it to shoulder height with both hands with your arms extended in front of you. Adopt a wide stance. This will be your starting position.	1
7163	192	Perform the movement by rotating the trunk and hips as you swing the weight all the way down to one side. Keep your arms extended throughout the exercise.	2
7164	192	Reverse the motion to swing the weight all the way to the opposite side.	3
7165	192	Continue alternating the movement until the set is complete.	4
7166	193	Position a bar into landmine or, lacking one, securely anchor it in a corner. Load the bar to an appropriate weight and position the handle attachment on the bar.	0
7167	193	Raise the bar from the floor, taking the handles to your shoulders. This will be your starting position.	1
7168	193	In an athletic stance, squat by flexing your hips and setting your hips back, keeping your arms flexed.	2
7169	193	Reverse the motion by powerfully extending through the hips, knees, and ankles, while also extending the elbows to straighten the arms. This movement should be done explosively, coming out of the squat to full extension as powerfully as possible.	3
7170	193	Return to the starting position.	4
7171	194	While lying on the floor, place a foam roll under your back and to one side, just behind your arm pit. This will be your starting position.	0
7172	194	Keep the arm of the side being stretched behind and to the side of you as you shift your weight onto your lats, keeping your upper body off of the ground. Hold for 10-30 seconds, and switch sides.	1
7173	195	Load the pins to an appropriate weight. Position yourself directly between the handles.	0
7174	195	Grasp the top handles with a comfortable grip, and then lower your hips as you take a breath. Look forward with your head and keep your chest up.	1
7175	195	Drive through the floor with your heels, extending your hips and knees as you rise to a standing position. Keep your arms straight throughout the movement, finishing with your shoulders back. This will be your starting position.	2
7176	195	Raise the weight by shrugging the shoulders towards your ears, moving straight up and down.	3
7177	195	Pause at the top of the motion, and then return the weight to the starting position.	4
7178	196	This drill helps you accelerate as quickly as possible into a sprint from a dead stop. It helps to use a line to start from. Begin with two feet on the line. Place your left foot with the toe next to your right ankle. Place your right foot 4-6 inches behind the left.	0
7180	196	Squat down as you lean foward, your head being lower than your hips and your weight loaded onto the left leg. This will be your starting position.	2
7181	196	Take your left hand up so that it is parallel to the ground, pointing behind you, and explode out when ready.	3
7182	197	Lean at around 45 degrees against a wall. Your feet should be together, glutes contracted.	0
7183	197	Begin by lifting your right knee quickly, pausing, and then driving it straight down into the ground.	1
7184	197	Switch legs, raising the opposite knee, and then attacking the ground straight down.	2
7185	197	Repeat once more with your right leg, and as soon as the right foot strikes the ground hammer them out rapidly, alternating left and right as fast as you can.	3
7186	224	Hook a leather ankle cuff to a low cable pulley and then attach the cuff to your ankle.	0
7187	224	Face the weight stack from a distance of about two feet, grasping the steel frame for support.	1
7442	285	With the bar at thigh level, load an appropriate weight.	0
7188	224	While keeping your knees and hips bent slightly and your abs tight, contract your glutes to slowly kick the working leg back in a semicircular arc as high as it will comfortably go as you breathe out. Tip: At full extension, squeeze your glutes for a second in order to achieve a peak contraction.	2
7189	224	Now slowly bring your working leg forward, resisting the pull of the cable until you reach the starting position.	3
7190	224	Repeat for the recommended amount of repetitions.	4
7191	224	Switch legs and repeat the movement for the other side.	5
7192	198	Begin standing with the log in front of you. Grasp the handles, and begin to clean the log. As you are bent over to start the clean, attempt to get the log as high as possible, pulling it into your chest. Extend through the hips and knees to bring it up to complete the clean.	0
7193	198	Push your head back and look up, creating a shelf on your chest to rest the log. Begin the press by dipping, flexing slightly through the knees and reversing the motion. This push press will generate momentum to start the log moving vertically. Continue by extending through the elbows to press the log above your head. There are no strict rules on form, so use whatever techniques you are most efficient with. As the log is pressed, ensure that you push your head through on each repetition, looking forward.	1
7194	198	Repeat as many times as possible. Attempt to control the descent of the log as it is returned to the ground.	2
7195	199	Attach a climbing rope to a high beam or cross member. Below it, ensure that the smith machine bar is locked in place with the safeties and cannot move. Alternatively, a secure box could also be utilized.	0
7196	199	Stand on the bar, using the rope to balance yourself. This will be your starting position.	1
7197	199	Keeping your body straight, lean back and lower your body by slowly going hand over hand with the rope. Continue until you are perpendicular to the ground.	2
7198	199	Keeping your body straight, reverse the motion, going hand over hand back to the starting position.	3
7199	200	Kneel on the floor, holding your heels with both hands.	0
7200	200	Lift your buttocks up and forward while bringing your head back to look up at the ceiling, to give an arch in your back.	1
7201	201	To move into the starting position, place the pulleys at the low position, select the resistance to be used and grasp a handle in each hand.	0
7202	201	Step forward, gaining tension in the pulleys. Your palms should be facing forward, hands below the waist, and your arms straight. This will be your starting position.	1
7203	201	With a slight bend in your arms, draw your hands upward and toward the midline of your body. Your hands should come together in front of your chest, palms facing up.	2
7204	201	Return your arms back to the starting position after a brief pause.	3
7471	291	Keep your back and arms straight and core tight while you pivot your back foot and bend your knees to get a full range of motion.	4
7205	203	While holding a barbell or EZ Curl bar with a pronated grip (palms facing forward), lie on your back on a flat bench with your head off the end of the bench. Tip: If you are holding a barbell grab it using a shoulder-width grip and if you are using an E-Z Bar grab it on the inner handles.	0
7206	203	Extend your arms in front of you as you hold the barbell over your chest. The arms should be perpendicular to your torso (90-degree angle). This will be your starting position.	1
7207	203	As you inhale, lower the bar in a semi-circular motion by bending at the elbows and while keeping the upper arm stationary and elbows in. Keep lowering the bar until it lightly touches your chin.	2
7208	203	As you exhale bring the bar back up to the starting position by pushing the bar up in a semi-circular motion. Contract the triceps hard at the top of the movement for a second. Tip: Again, only the forearms should move. The upper arms should remain stationary at all times.	3
7209	203	Repeat for the recommended amount of repetitions.	4
7210	202	Lie on your back with your knees bent and the soles of the feet pressed together. Have your partner hold your knees. This will be your starting position.	0
7211	202	Attempt to squeeze your knees together, while your partner prevents any movement from occurring.	1
7212	202	After 10-20 seconds, relax your muscles as your partner gently pushes your knees towards the floor. Be sure to inform your helper when the stretch is adequate to prevent injury or overstretching.	2
7213	204	Lie on your back with your legs extended.	0
7214	204	Cross one leg over your body with the knee bent, attempting to touch the knee to the ground. Your partner should kneel beside you, holding your shoulder down with one hand and controlling the crossed leg with the other. this will be your starting position.	1
7215	204	Attempt to raise the bent knee off of the ground as your partner prevents any actual movement.	2
7216	204	After 10-20 seconds, relax the leg as your partner gently presses the knee towards the floor. Repeat with the other side.	3
7217	66	Lie on your back, with one leg extended straight out.	0
7218	66	With the other leg, bend the hip and knee to 90 degrees. You may brace your leg with your hands if necessary. This will be your starting position.	1
7219	66	Extend your leg straight into the air, pausing briefly at the top. Return the leg to the starting position.	2
7220	66	Repeat for 10-20 repetitions, and then switch to the other leg.	3
7221	210	Sit down on the Preacher Curl Machine and select the weight.	0
7222	210	Place the back of your upper arms (your triceps) on the preacher pad provided and grab the handles using an underhand grip (palms facing up). Tip: Make sure that when you place the arms on the pad you keep the elbows in. This will be your starting position.	1
7223	210	Now lift the handles as you exhale and you contract the biceps. At the top of the position make sure that you hold the contraction for a second. Tip: Only the forearms should move. The upper arms should remain stationary and on the pad at all times.	2
7224	210	Lower the handles slowly back to the starting position as you inhale.	3
7225	210	Repeat for the recommended amount of repetitions.	4
7226	364	Being in a standing position. Jump into a split leg position, with one leg forward and one leg back, flexing the knees and lowering your hips slightly as you do so.	0
7227	364	As you descend, immediately reverse direction, standing back up and jumping, reversing the position of your legs. Repeat 5-10 times on each leg.	1
7228	68	Lie face down with one leg on a foam roll.	0
7229	68	Rotate the leg so that the foam roll contacts against your inner thigh. Shift as much weight onto the foam roll as can be tolerated.	1
7230	68	While trying to relax the muscles if the inner thigh, roll over the foam between your hip and knee, holding points of tension for 10-30 seconds. Repeat with the other leg.	2
7231	209	Lay face down on the floor with your partner kneeling beside you. Flex one knee and raise that leg off the ground, attempting to touch your glutes with your foot. Your partner should hold the knee and ankle. This will be your starting position.	0
7232	209	Attempt to extend your knee while your partner prevents any actual movement.	1
7233	209	After 10-20 seconds, relax your muscles as your partner gently pushes the foot towards your glutes, further stretching the quadriceps and hip flexors.	2
7234	209	After 10-20 seconds, switch sides.	3
7235	211	Using a spacing that is just about 1 inch wider than shoulder width, grab a pull-up bar with the palms of one hand facing forward and the palms of the other hand facing towards you. This will be your starting position.	0
7236	211	Now start to pull yourself up as you exhale. Tip: With the arm that has the palms facing up concentrate on using the back muscles in order to perform the movement. The elbow of that arm should remain close to the torso. With the other arm that has the palms facing forward, the elbows will be away but in line with the torso. You will concentrate on using the lats to pull your body up.	1
7237	211	After a second contraction at the top, start to slowly come down as you inhale.	2
7238	211	Repeat for the recommended amount of repetitions.	3
7239	211	On the following set, switch grips; so if you had the right hand with the palms facing you and the left one with the palms facing forward, on the next set you will have the palms facing forward for the right hand and facing you for the left.	4
7240	212	Place a band around both ankles and another around both knees. There should be enough tension that they are tight when your feet are shoulder width apart.	0
7241	212	To begin, take short steps forward alternating your left and right foot.	1
7242	212	After several steps, do just the opposite and walk backward to where you started.	2
7245	214	This move helps prepare your running form to help you excel at sprinting. As you run, be sure to flex the knee, aiming to kick your glutes as the hip extends.	0
7246	214	Reload the quad as the leg moves back forward, attacking the ground on the next step.	1
7247	214	Ensure that as you run, you block with the arms, punching through in a rapid 1-2 motion.	2
7248	331	Sit upright on a chair.	0
7249	331	Bend to one side with your arm over your head. You can hold onto the chair with your free hand.	1
7250	331	Hold for 10 seconds, and repeat for your other side.	2
7251	215	Using a muscle roller or a rolling pin, place the roller behind your head and against your neck. Make sure that you do not place the roller directly against the spine, but turned slightly so that the roller is pressed against the muscles to either side of the spine. This will be your starting position.	0
7252	215	Starting at the top of your neck, slowly roll down the muscles of your neck, pausing at points of tension for 10-30 seconds.	1
7253	230	Pin presses remove the eccentric phase of the bench press, developing starting strength. They also allow you to train a desired range of motion.	0
7254	230	The bench should be set up in a power rack. Set the pins to the desired point in your range of motion, whether it just be lockout or an inch off of your chest. The bar should be moved to the pins and prepared for lifting.	1
7255	230	Begin by lying on the bench, with the bar directly above the contact point during your regular bench. Tuck your feet underneath you and arch your back. Using the bar to help support your weight, lift your shoulder off the bench and retract them, squeezing the shoulder blades together. Use your feet to drive your traps into the bench. Maintain this tight body position throughout the movement.	2
7256	230	You can take a standard bench grip, or shoulder width to focus on the triceps. The bar, wrist, and elbow should stay in line at all times. Focus on squeezing the bar and trying to pull it apart.	3
7257	230	Drive the bar up with as much force as possible. The elbows should be tucked in until lockout.	4
7258	230	Return the bar to the pins, pausing before beginning the next repetition.	5
7259	232	Grab two wide-rimmed plates and put them together with the smooth sides facing outward	0
7260	232	Use your fingers to grip the outside part of the plate and your thumb for the other side thus holding both plates together. This is the starting position.	1
7261	232	Squeeze the plate with your fingers and thumb. Hold this position for as long as you can.	2
7262	232	Repeat for the recommended amount of sets prescribed in your program.	3
7263	232	Switch arms and repeat the movements.	4
7264	233	Lie down on the floor or an exercise mat with your legs fully extended and your upper body upright. Grab the plate by its sides with both hands out in front of your abdominals with your arms slightly bent.	0
7347	256	Reverse the motion by extending the hips, kicking the leg back. It is very important not to over-extend the hip on this movement, stopping short of your full range of motion.	2
7265	233	Slowly cross your legs near your ankles and lift them up off the ground. Your knees should also be bent slightly. Note: Move your upper body back slightly to help keep you balanced turning this exercise. This is the starting position.	1
7266	233	Move the plate to the left side and touch the floor with it. Breathe out as you perform that movement.	2
7267	233	Come back to the starting position as you breathe in and then repeat the movement but this time to the right side of the body. Tip: Use a slow controlled movement at all times. Jerking motions can injure the back.	3
7268	233	Repeat for the recommended amount of repetitions.	4
7269	234	For this movement a wooden floor or similar is needed. Lay on your back with your legs extended. Place a gym towel or a light weight underneath your heel. This will be your starting position.	0
7270	234	Begin the movement by flexing the knee, keeping your other leg straight.	1
7271	234	Continue bringing the heel closer to you, sliding it on the floor.	2
7272	234	At full knee flexion, reverse the movement to return to the starting position.	3
7273	236	You will need a partner for this exercise. Lay face down with your legs straight. Your assistant will place their hand on your heel.	0
7274	236	To begin, flex the knee to curl your leg up. Your partner should provide resistance, starting light and increasing the pressure as the movement is completed. Communicate with your partner to monitor appropriate resistance levels.	1
7275	236	Pause at the top, returning the leg to the starting position as your partner provides resistance going the other direction.	2
7290	241	Standing with the weight racked on the back of the shoulders, begin with the dip. With your feet directly under your hips, flex the knees without moving the hips backward. Go down only slightly, and reverse direction as powerfully as possible. Drive through the heels create as much speed and force as possible, moving the bar in a vertical path.	0
7291	241	Using the momentum generated, finish pressing the weight overhead be extending through the arms.	1
7292	241	Return to the starting position, using your legs to absorb the impact.	2
7293	243	Lie on the floor face down and body straight with your toes on the floor and the hands wider than shoulder width for a wide hand position and closer than shoulder width for a close hand position. Make sure you are holding your torso up at arms length.	0
7294	243	Lower yourself until your chest almost touches the floor as you inhale.	1
7295	243	Using your pectoral muscles, press your upper body back up to the starting position and squeeze your chest. Breathe out as you perform this step.	2
7296	243	After a second pause at the contracted position, repeat the movement for the prescribed amount of repetitions.	3
7297	244	Start off by rolling your torso forward onto the ball so your hips rest on top of the ball and become the highest point of your body.	0
7298	244	Rest your hands and feet on the floor. Your arms and legs can be slightly bent or straight, depending on the size of the ball, your flexibility, and the length of your limbs. This also helps develop stabilizing strength in your torso and shoulders.	1
7299	246	You will need a box for this exerise.	0
7300	246	Begin facing the box standing 1-2 feet from its edge.	1
7301	246	By utilizing your hips, hop onto the box, landing on both legs. Ensure that you land with your legs bent and your feet flat.	2
7302	246	Immediately upon landing, fully extend through the entire body and swing your arms overhead to explode off of the box. Use your legs to absorb the impact of landing.	3
7303	247	This drill teaches the delivery of the barbell to the rack position on the shoulders. Begin holding a bar in the scarecrow position, with the upper arms parallel to the floor, and the forearms hanging down. Use a hook grip, with your fingers wrapped over your thumbs.	0
7304	247	Begin by rotating the elbows around the bar, delivering the bar to the shoulders. As your elbows come forward, relax your grip. The shoulders should be protracted, providing a shelf for the bar, which should lightly contact the throat.	1
7305	247	It is important that the bar stay close to the body at all times, as with a heavier load any distance will result in an unwanted collision. As the movement becomes smoother, speed and load can be increased before progressing further.	2
7306	248	Set up in a power rack with the bar on the pins. The pins should be set to the desired point; just below the knees, just above, or in the mid thigh position. Position yourself against the bar in proper deadlifting position. Your feet should be under your hips, your grip shoulder width, back arched, and hips back to engage the hamstrings. Since the weight is typically heavy, you may use a mixed grip, a hook grip, or use straps to aid in holding the weight.	0
7307	248	With your head looking forward, extend through the hips and knees, pulling the weight up and back until lockout. Be sure to pull your shoulders back as you complete the movement.	1
7308	248	Return the weight to the pins and repeat.	2
7309	250	You will need a partner for this drill.	0
7310	250	Begin in an athletic 2 or 3 point stance.	1
7311	250	At the signal, move into a position to receive the pass from your partner.	2
7312	250	Catch the medicine ball with both hands and immediately throw it back to your partner.	3
7313	250	You can modify this drill by running different routes.	4
7314	251	Grab an EZ-bar using a shoulder width and palms down (pronated) grip.	0
7315	251	Now place the upper part of both arms on top of the preacher bench and have your arms extended. This will be your starting position.	1
7316	251	As you exhale, use the biceps to curl the weight up until your biceps are fully contracted and the barbell is at shoulder height. Squeeze the biceps hard for a second at the contracted position.	2
7317	251	As you breathe in, slowly lower the barbell until your upper arms are extended and the biceps is fully stretched.	3
7318	251	Repeat for the recommended amount of repetitions.	4
7319	252	Lie down on the floor with your legs fully extended and arms to the side of your torso with the palms on the floor. Your arms should be stationary for the entire exercise.	0
7320	252	Move your legs up so that your thighs are perpendicular to the floor and feet are together and parallel to the floor. This is the starting position.	1
7321	252	While inhaling, move your legs towards the torso as you roll your pelvis backwards and you raise your hips off the floor. At the end of this movement your knees will be touching your chest.	2
7322	252	Hold the contraction for a second and move your legs back to the starting position while exhaling.	3
7323	252	Repeat for the recommended amount of repetitions.	4
7330	249	To begin, seat yourself on the bike and adjust the seat to your height.	0
7331	249	Select the desired option from the menu. You may have to start pedaling to turn it on. You can use the manual setting, or you can select a program to use. Typically, you can enter your age and weight to estimate the amount of calories burned during exercise. The level of resistance can be changed throughout the workout. The handles can be used to monitor your heart rate to help you stay at an appropriate intensity.	1
7332	249	Recumbent bikes offer convenience, cardiovascular benefits, and have less impact than other activities. A 150 lb person will burn about 230 calories cycling at a moderate rate for 30 minutes, compared to 450 calories or more running.	2
7472	291	Maintain your stance and straight arms. Return to the neutral position in a slow and controlled manner.	5
7340	255	Stand erect while holding a barbell with a supinated grip (palms facing up).	0
7341	255	Bend your knees slightly and bring your torso forward, by bending at the waist, while keeping the back straight until it is almost parallel to the floor. Tip: Make sure that you keep the head up. The barbell should hang directly in front of you as your arms hang perpendicular to the floor and your torso. This is your starting position.	1
7342	255	While keeping the torso stationary, lift the barbell as you breathe out, keeping the elbows close to the body and not doing any force with the forearm other than holding the weights. On the top contracted position, squeeze the back muscles and hold for a second.	2
7343	255	Slowly lower the weight again to the starting position as you inhale.	3
7344	255	Repeat for the recommended amount of repetitions.	4
7345	256	Place your feet between the pads after loading an appropriate weight. Lay on the top pad, allowing your hips to hang off the back, while grasping the handles to hold your position.	0
7346	256	To begin the movement, flex the hips, pulling the legs forward.	1
7348	256	Return by again flexing the hip, pulling the carriage forward as far as you can.	3
7350	257	Adjust the handles so that they are fully to the rear. Make an appropriate weight selection and adjust the seat height so the handles are at shoulder level. Grasp the handles with your hands facing inwards. This will be your starting position.	0
7351	257	In a semicircular motion, pull your hands out to your side and back, contracting your rear delts.	1
7352	257	Keep your arms slightly bent throughout the movement, with all of the motion occurring at the shoulder joint.	2
7353	257	Pause at the rear of the movement, and slowly return the weight to the starting position.	3
7354	258	Start by standing straight with a weighted plate held by both hands and arms fully extended. Use a pronated grip (palms facing down) and make sure your fingers grab the rough side of the plate while your thumb grabs the smooth side. Note: For the best results, grab the weighted plate at an 11:00 and 1:00 o'clock position.	0
7355	258	Your feet should be shoulder width apart from each other and the weighted plate should be near the groin area. This is the starting position.	1
7356	258	Slowly lift the plate up while keeping the elbows in and the upper arms stationary until your biceps and forearms touch while exhaling. The plate should be evenly aligned with your torso at this point.	2
7357	258	Feel the contraction for a second and begin to lower the weight back down to the starting position while inhaling	3
7358	258	Repeat for the recommended amount of repetitions.	4
7363	261	Grab the rope with both hands above your head. Pull down on the rope as you take a small jump.	0
7364	261	Wrap the rope around one leg, using your feet to pinch the rope. Reach up as high as possible with your arms, gripping the rope tightly.	1
7365	261	Release the rope from your feet as you pull yourself up with your arms, bringing your knees towards your chest.	2
7366	261	Resecure your feet on the rope, and then stand up to take another high hold on the rope. Continue until you reach the top of the rope.	3
7367	261	To lower yourself, loosen the grip of your feet on the rope as you slide down using a hand over hand motion.	4
7368	265	Lie down on the floor placing your feet either under something that will not move or by having a partner hold them. Your legs should be bent at the knees.	0
7369	265	Elevate your upper body so that it creates an imaginary V-shape with your thighs. Your arms should be fully extended in front of you perpendicular to your torso and with the hands clasped. This is the starting position.	1
7370	265	Twist your torso to the right side until your arms are parallel with the floor while breathing out.	2
7371	265	Hold the contraction for a second and move back to the starting position while breathing out. Now move to the opposite side performing the same techniques you applied to the right side.	3
7372	265	Repeat for the recommended amount of repetitions.	4
7373	266	To load sandbags or other objects, begin with the implements placed a distance from the loading platform, typically 50 feet.	0
7374	266	Begin by lifting the sandbag. Sandbags are extremely awkward, and the manner of lifting them can vary depending on the particular sandbag used. Reach as far around it as possible, extending through the hips and knees to pull it up high. Shouldering is usually not allowed.	1
7375	266	Move as quickly as possible to the platform, and load it, extending through your hips, knees, and ankles to get it as high as possible. Place it onto the platform, ensuring it doesn't fall off.	2
7376	266	Return to the starting position to retrieve the next sandbag, and repeat until the event is completed.	3
7377	268	Start out by sitting at the end of a flat bench with a barbell placed on top of your thighs. Your feet should be shoulder width apart from each other.	0
7378	268	Grip the bar with your palms facing down and make sure your hands are wider than shoulder width apart from each other. Begin to lift the barbell up over your head until your arms are fully extended.	1
7379	268	Now lower the barbell behind your head until it is resting along the base of your neck. This is the starting position.	2
7380	268	While keeping your feet and head stationary, move your waist from side to side so that your oblique muscles feel the contraction. Only move from side to side as far as your waist will allow you to go. Stretching or moving too far can cause an injury to occur. Tip: Use a slow and controlled motion.	3
7473	291	Repeat to failure.	6
7381	268	Remember to breathe out while twisting your body to the side and in when moving back to the starting position.	4
7382	268	Repeat for the recommended amount of repetitions.	5
7383	279	Lay on the floor with your feet flat and knees bent.	0
7384	279	Raise one leg off of the ground, pulling the knee to your chest. This will be your starting position.	1
7385	279	Execute the movement by driving through the heel, extending your hip upward and raising your glutes off of the ground.	2
7386	279	Extend as far as possible, pause and then return to the starting position.	3
7387	267	To begin, lie down with your back pressed against the floor or on an exercise mat (optional). Your arms should be fully extended to the sides with your palms facing down. Note: The arms should be stationary the entire time.	0
7388	267	With a slight bend at the knees, lift your legs up so that your heels are about 6 inches off the ground. This is the starting position.	1
7389	267	Now lift your left leg up to about a 45 degree angle while your right leg is lowered until the heel is about 2-3 inches from the ground.	2
7390	267	Switch movements by raising your right leg up and lowering your left leg. Remember to breathe while performing this exercise.	3
7391	267	Repeat for the recommended amount of repetitions.	4
7392	272	Place a neck strap on the floor at the end of a flat bench. Once you have selected the weights, sit at the end of the flat bench with your feet wider than shoulder width apart from each other. Your toes should be pointed out.	0
7432	282	Return to the starting position, taking a couple steps back to take the slack out of the line.	3
7393	272	Slowly move your torso forward until it is almost parallel with the floor. Using both hands, securely position the neck strap around your head. Tip: Make sure the weights are still lying on the floor to prevent any strain on the neck. Now grab the weight with both hands while elevating your torso back until it is almost perpendicular to the floor. Note: Your head and torso needs to be slightly tilted forward to perform this exercise.	1
7394	272	Now place both hands on top of your knees. This is the starting position.	2
7395	272	Slowly lower your neck down until your chin touches the upper part of your chest while breathing in.	3
7396	272	While exhaling, bring your neck back to the starting position.	4
7397	272	Repeat for the recommended amount of repetitions.	5
7398	273	To get into the starting position, first sit down on the machine and place your feet on the front platform or crossbar provided making sure that your knees are slightly bent and not locked.	0
7399	273	Lean over as you keep the natural alignment of your back and grab the single handle attachment with your left arm using a palms-down grip.	1
7400	273	With your arm extended pull back until your torso is at a 90-degree angle from your legs. Your back should be slightly arched and your chest should be sticking out. You should be feeling a nice stretch on your lat as you hold the bar in front of you. The right arm can be kept by the waist. This is the starting position of the exercise.	2
7401	273	Keeping the torso stationary, pull the handles back towards your torso while keeping the arms close to it as you rotate the wrist, so that by the time your hand is by your abdominals it is in a neutral position (palms facing the torso). Breathe out as you perform that movement. At that point you should be squeezing your back muscles hard.	3
7402	273	Hold that contraction for a second and slowly go back to the original position while breathing in. Tip: Remember to rotate the wrist as you go back to the starting position so that the palms are facing down again.	4
7403	273	Repeat for the recommended amount of repetitions and then perform the same movement with the right hand.	5
7404	274	Grab the pull-up bar with the palms facing forward using a wide grip.	0
7405	274	As you have both arms extended in front of you holding the bar at a wide grip, bring your torso back around 30 degrees or so while creating a curvature on your lower back and sticking your chest out. This is your starting position.	1
7406	274	Pull your torso up while leaning to the left hand side until the bar almost touches your upper chest by drawing the shoulders and the upper arms down and back. Exhale as you perform this portion of the movement. Tip: Concentrate on squeezing the back muscles once you reach the full contracted position. The upper torso should remain stationary as it moves through space (no swinging) and only the arms should move. The forearms should do no other work other than hold the bar.	2
7407	274	After a second of contraction, inhale as you go back to the starting position.	3
7408	274	Now, pull your torso up while leaning to the right hand side until the bar almost touches your upper chest by drawing the shoulders and the upper arms down and back. Exhale as you perform this portion of the movement. Tip: Concentrate on squeezing the back muscles once you reach the full contracted position. The upper torso should remain stationary as it moves through space and only the arms should move. The forearms should do no other work other than hold the bar.	4
7409	274	After a second of contraction, inhale as you go back to the starting position.	5
7410	274	Repeat steps 3-6 until you have performed the prescribed amount of repetitions for each side.	6
7411	275	Begin by moving the pulleys to the high position, select the resistance to be used, and take a handle in each hand.	0
7412	275	Step forward in front of both pulleys with your arms extended in front of you, bringing your hands together. Your head and chest should be up as you lean forward, while your feet should be staggered. This will be your starting position.	1
7413	275	Keeping your left arm in place, allow your right arm to extend out to the side, maintaining a slight bend at the elbow. The right arm should be perpendicular to the body at approximately shoulder level.	2
7414	275	Return your arm back to the starting position by pulling your hand back to the midline of the body.	3
7415	275	Hold for a second at the starting position and repeat the movement on the opposite side. Continue alternating back and forth for the prescribed number of repetitions.	4
7416	276	Position a bar into a landmine or securely anchor it in a corner. Load the bar to an appropriate weight.	0
7417	276	Raise the bar from the floor, taking it to your shoulders with one or both hands. Adopt a wide stance. This will be your starting position.	1
7418	276	Perform the movement by extending the elbow, pressing the weight up. Move explosively, extending the hips and knees fully to produce maximal force.	2
7419	276	Return to the starting position.	3
7420	277	This drill teaches quick foot action. You need a single cone. Begin standing next to the cone with one arm back and one arm forward.	0
7421	277	Chop the feet as quickly as possible, blocking with the arms. Circle the cone, keep your knees up, with violent foot action.	1
7422	277	Rest after three trips around the cone.	2
7423	278	Begin by standing on one leg, with the bent knee raised. This will be your start position.	0
7424	278	Using a countermovement jump, take off upward by extending the hip, knee, and ankle of the grounded leg.	1
7425	278	Immediately flex the knee and attempt to touch your butt with the heel of your jumping leg.	2
7426	278	Return the leg to a partially bent position underneath the hips and land. Your opposite leg should stay in relatively the same position throughout the drill.	3
7427	281	To begin, load the sled with the desired weight and attach the pulling strap. You can pull with handles, use a harness, or attach the pulling strap to a weight belt.	0
7428	281	Whether pulling forwards or backwards, lean in the direction of travel and progress by extending through the hips and knees.	1
7429	282	Attach dual handles to a sled connected by a rope or chain. Load the sled to a light weight.	0
7430	282	Face the sled, backing up until there is some tension in the line. Take both handles at arms length at about waist level. Bend the knees slightly and keep your chest and head up. This will be your starting position.	1
7431	282	Without flexing the elbow, pull the handles upward and apart, performing a reverse fly with some external rotation. Your palms should be facing forward as you do this.	2
7433	283	You will need a tire and a sledgehammer for this exercise. Stand in front of the tire about two feet away from it with a staggered stance. Grip the sledgehammer.	0
7434	283	If you are right handed, your left hand should be at the bottom of the handle, and your right hand should be choking up closer to the head.	1
7435	283	As you bring the sledge up, your right hand slides toward the head; as you swing down, your right hand will slide down to join your left hand. Slam it down as hard as you can against the tire. Control the bounce of the hammer off of the tire.	2
7436	283	Repeat on the other side.	3
7437	284	With the bar at thigh level, load an appropriate weight.	0
7438	284	Stand with the bar behind you, taking a shoulder-width, pronated grip on the bar and unhook the weight. You should be standing up straight with your head and chest up and your arms extended. This will be your starting position.	1
7443	285	Take a wide grip on the bar and unhook the weight, removing your off hand from the bar. Your arm should be extended as you stand up straight with your head and chest up. This will be your starting position.	1
7444	285	Begin the movement by flexing the elbow, raising the upper arm with the elbow pointed out. Continue until your upper arm is parallel to the floor.	2
7445	285	After a brief pause, return the weight to the starting position.	3
7446	285	Repeat for the desired number of repetitions before engaging the hooks to rack the weight.	4
7447	286	Hold a dumbbell in each hand with a pronated grip. Your feet should be wide with your hips and knees extended. This will be your starting position.	0
7448	286	Begin the movement by pulling both of the dumbbells to one side next to your hip, rotating your torso.	1
7449	286	Keeping your arms straight and the dumbbells parallel to the ground, rotate your torso to swing the weights to your opposite side.	2
7450	286	Continue alternating, rotating from one side to the other until the set is complete.	3
7451	287	Begin in a prone position on the floor. Support your weight on your hands and toes, with your feet together and your body straight. Your arms should be bent to 90 degrees. This will be your starting position.	0
7452	287	Initiate the movement by raising one foot off of the ground. Externally rotate the leg and bring the knee toward your elbow, as far forward as possible.	1
7453	287	Return this leg to the starting position and repeat on the opposite side.	2
7454	308	Begin by gripping the bottom of the tire on the tread, and position your feet back a bit. Your chest should be driving into the tire.	0
7455	308	To lift the tire, extend through the hips, knees, and ankles, driving into the tire and up.	1
7456	308	As the tire reaches a 45 degree angle, step forward and drive a knee into the tire. As you do so adjust your grip to the upper portion of the tire and push it forward as hard as possible to complete the turn. Repeat as necessary.	2
7457	280	Roller skating is a fun activity which can be effective in improving cardiorespiratory fitness and muscular endurance. It requires relatively good balance and coordination. It is necessary to learn the basics of skating including turning and stopping and to wear protective gear to avoid possible injury.	0
7458	280	You can skate at a comfortable pace for 30 minutes straight. If you want a cardio challenge, do interval skating  speed skate two minutes of every five minutes, using the remaining three minutes to recover. A 150 lb person will typically burn about 175 calories in 30 minutes skating at a comfortable pace, similar to brisk walking.	1
7459	290	Connect a standard handle on a tower, and move the cable to the lowest pulley position.	0
7460	290	With your side to the cable, grab the handle with one hand and step away from the tower. You should be approximately arm length away from the pulley, with the tension of the weight on the cable. Your outstretched arm should be aligned with the cable.	1
7461	290	With your feet positioned shoulder width apart, squat down and grab the handle with both hands. Your arms should still be fully extended.	2
7462	290	In one motion, pull the handle up and across your body until your arms are in a fully-extended position above your head.	3
7463	290	Keep your back straight and your arms close to your body as you pivot your back foot and straighten your legs to get a full range of motion.	4
7464	290	Retract your arms and then your body. Return to the neutral position in a slow and controlled manner.	5
7465	290	Repeat to failure.	6
7466	290	Then, reposition and repeat the same series of movements on the opposite side.	7
7467	291	Connect a standard handle to a tower, and move the cable to the highest pulley position.	0
7468	291	With your side to the cable, grab the handle with one hand and step away from the tower. You should be approximately arm length away from the pulley, with the tension of the weight on the cable. Your outstretched arm should be aligned with the cable.	1
7475	292	To begin, stand straight while holding a weight plate by the ridge at arm's length in each hand using a neutral grip (palms facing in). You feet should be shoulder width apart from each other. This will be your starting position.	0
7476	292	Lower the plates until the fingers are nearly extended but can still hold weights. Inhale as you lower the plates.	1
7477	292	Now raise the plates back to the starting position as you exhale by closing your hands.	2
7478	292	Repeat for the recommended amount of repetitions prescribed in your program.	3
7479	295	Stand with your feet shoulder width apart holding a medicine ball in both hands. To begin, reach the medicine ball deep behind your head as you bend the knees slightly and lean back.	0
7480	295	Violently throw the ball forward, flexing at the hip and using your whole body to complete the movement.	1
7481	295	The medicine ball can be thrown to a partner or to a wall, receiving it as it bounces back.	2
7482	293	Start off with your feet hip-distance apart.	0
7483	293	Bend your knees slightly to keep them soft and springy.	1
7484	293	You may want to move your pelvis forward and backward and back few times before holding the tailbone forward in this stretch.	2
7485	298	Place a dumbbell standing up on a flat bench.	0
7486	298	Ensuring that the dumbbell stays securely placed at the top of the bench, lie perpendicular to the bench (torso across it as in forming a cross) with only your shoulders lying on the surface. Hips should be below the bench and legs bent with feet firmly on the floor. The head will be off the bench as well.	1
7487	298	Grasp the dumbbell with both hands and hold it straight over your chest at arms length. Both palms should be pressing against the underside one of the sides of the dumbbell. This will be your starting position.Caution: Always ensure that the dumbbell used for this exercise is secure. Using a dumbbell with loose plates can result in the dumbbell falling apart and falling on your face.	2
7488	298	While keeping your arms straight, lower the weight slowly in an arc behind your head while breathing in until you feel a stretch on the chest.	3
7489	298	At that point, bring the dumbbell back to the starting position using the arc through which the weight was lowered and exhale as you perform this movement.	4
7490	298	Hold the weight on the initial position for a second and repeat the motion for the prescribed number of repetitions.	5
7491	300	This drill is great for chest passes when you lack a partner or a wall of sufficient strength. Lay on the ground on your back with your knees bent.	0
7492	300	Begin with the ball on your chest, held with both hands on the bottom.	1
7493	300	Explode up, extending through the elbow to throw the ball directly above you as high as possible.	2
7494	300	Catch the ball with both hands as it comes down.	3
7495	301	Lay on the ground on your back with your knees bent. Hold the ball with one hand, extending the arm fully behind your head. This will be your starting position.	0
7496	301	Initiate the movement at the shoulder, throwing the ball directly forward of you as you sit up, attempting to go for maximum distance.	1
7497	301	The ball can be thrown to a partner or bounced off of a wall.	2
7498	302	Lay on the ground on your back with your knees bent.	0
7499	302	Hold the ball with both hands, extending the arms fully behind your head. This will be your starting position.	1
7500	302	Initiate the movement at the shoulder, throwing the ball directly forward of you as you sit up, attempting to go for maximum distance.	2
7501	302	The ball can be thrown to a partner or bounced off of a wall.	3
7502	303	Adjust the straps so the handles are at an appropriate height, below waist level.	0
7503	303	Begin standing and grasping the handles. Lean into the straps, moving to an incline push-up position. This will be your starting position.	1
7504	303	Keeping your arms straight, lean further into the suspension straps, bringing your body closer to the ground, allowing your shoulders to extend, raising your arms up and over your head.	2
7505	303	Maintain a neutral spine and keep the rest of your body straight, your shoulders being the only joints allowed to move.	3
7506	303	Pause during the peak contraction, and then return to the starting position.	4
7507	304	Secure a set of suspension straps with the handles hanging about a foot off of the ground. Move yourself into a pushup plank position facing away from the rack.	0
7508	304	Place your feet into the handles. You should maintain a straight posture, not allowing the hips to sag. This will be your starting position.	1
7509	304	Begin the movement by flexing the knees and hips, drawing the knees to your torso. As you do so, anteriorly tilt your pelvis, allowing your spine to flex.	2
7510	304	At the top of the controlled motion, return to the starting position.	3
7511	306	To begin, sit down on the abductor machine and select a weight you are comfortable with. When your legs are positioned properly, grip the handles on each side. Your entire upper body (from the waist up) should be stationary. This is the starting position.	0
7512	306	Slowly press against the machine with your legs to move them away from each other while exhaling.	1
7513	306	Feel the contraction for a second and begin to move your legs back to the starting position while breathing in. Note: Remember to keep your upper body stationary to prevent any injuries from occurring.	2
7514	306	Repeat for the recommended amount of repetitions.	3
7515	307	To begin, sit down on the adductor machine and select a weight you are comfortable with. When your legs are positioned properly on the leg pads of the machine, grip the handles on each side. Your entire upper body (from the waist up) should be stationary. This is the starting position.	0
7516	307	Slowly press against the machine with your legs to move them towards each other while exhaling.	1
7517	307	Feel the contraction for a second and begin to move your legs back to the starting position while breathing in. Note: Remember to keep your upper body stationary and avoid fast jerking motions in order to prevent any injuries from occurring.	2
7518	307	Repeat for the recommended amount of repetitions.	3
7519	310	To begin, lie down on the floor or an exercise mat with your back pressed against the floor. Your arms should be lying across your sides with the palms facing down.	0
7284	16	After a second pause at the contracted position, repeat the movement for the prescribed amount of repetitions.	3
7520	310	Your legs should be crossed by wrapping one ankle around the other. Slowly elevate your legs up in the air until your thighs are perpendicular to the floor with a slight bend at the knees. Note: Your knees and toes should be parallel to the floor as opposed to the thighs.	1
7521	310	Move your arms from the floor and cross them so they are resting on your chest. This is the starting position.	2
7522	310	While keeping your lower back pressed against the floor, slowly lift your torso. Remember to exhale while perform this part of the exercise.	3
7523	310	Slowly begin to lower your torso back down to the starting position while inhaling.	4
7524	310	Repeat for the recommended amount of repetitions.	5
7530	312	To begin, lie down on an exercise ball with your torso pressing against the ball and parallel to the floor. The ball of your feet should be pressed against the floor to help keep you balanced. Place a weighted plate under your chin or behind your neck. This is the starting position.	0
7531	312	Slowly raise your torso up by bending at the waist and lower back. Remember to exhale during this movement.	1
7532	312	Hold the contraction on your lower back for a second and lower your torso back down to the starting position while inhaling.	2
7533	312	Repeat for the recommended amount of repetitions prescribed in your program.	3
7534	313	Lie flat on your back with your feet flat on the ground or resting on a bench with your knees bent at a 90 degree angle.	0
7535	313	Hold a weight to your chest, or you may hold it extended above your torso. This will be your starting position.	1
7536	313	Now, exhale and slowly begin to roll your shoulders off the floor. Your shoulders should come up off the floor about 4 inches while your lower back remains on the floor.	2
7537	313	At the top of the movement, flex your abdominals and hold for a brief pause.	3
7538	313	Then inhale and slowly lower yourself back down to the starting position.	4
7528	624	After a second hold on the contracted position, slowly lower your body back to the starting position as you breathe in.	3
7539	314	Start out by strapping the bands around the base of the decline bench. Place the handles towards the inside of the decline bench so that when lying down, you can reach for both of them.	0
7540	314	Position your legs through the decline machine until they are secured. Now reach for the exercise bands with both hands. Use a pronated (palms forward) grip to grasp the handles. Position them near your collar bone and rotate your wrist to a neutral grip (palms facing the torso). Note: Your arms should remain stationary throughout the exercise. This is the starting position.	1
7541	314	Move your torso upward until your upper body is perpendicular to the floor while exhaling. Hold the contraction for a second and lower your upper body back down to the starting position while inhaling.	2
7542	314	Repeat for the recommended amount of repetitions.	3
7543	315	Lie down on a decline bench with both legs securely locked in position. Reach for the barbell behind the head using a pronated grip (palms facing out). Make sure to grab the barbell wider than shoulder width apart for this exercise. Slowly lift the barbell up from the floor by using your arms.	0
7544	315	When positioned properly, your arms should be fully extended and perpendicular to the floor. This is the starting position.	1
7545	315	Begin by moving the barbell back down in a semicircular motion as if you were going to place it on the floor, but instead, stop when the arms are parallel to the floor. Tip: Keep the arms fully extended at all times. The movement should only happen at the shoulder joint. Inhale as you perform this portion of the movement.	2
7546	315	Now bring the barbell up while exhaling until you are back at the starting position. Remember to keep full control of the barbell at all times.	3
7547	315	Repeat the movement for the prescribed amount of repetitions of your training program.	4
7548	315	When finished with your set, slowly lower the barbell back down until it is level with your head and release it.	5
7549	316	Begin with a barbell loaded on the floor. Adopt a wide stance, and then bend at the hips to grab the bar. Your hips should be as far back as possible, and your legs nearly straight. Keep your back straight, and your head and chest up. This will be your starting position.	0
7550	316	Begin the movement be engaging the hips, driving them forward as you allow the arms to hang straight. Continue until you are standing straight up, and then slowly return the weight to the starting position. For successive reps, the weight need not touch the floor.	1
7551	317	Hang from a pull-up bar using a pronated grip. Your arms and legs should be extended. This will be your starting position.	0
7552	317	Begin by quickly raising one knee as high as you can. Do not swing your body or your legs. 3	1
7553	317	Immediately reverse the motion, returning that leg to the starting position. Simultaneously raise the opposite knee as high as possible.	2
7554	317	Continue alternating between legs until the set is complete.	3
7555	320	To begin, stand straight up grabbing a wrist roller using a pronated grip (palms facing down). Your feet should be shoulder width apart.	0
7556	320	Slowly lift both arms until they are fully extended and parallel to the floor in front of you. Note: Make sure the rope is not wrapped around the roller. Your entire body should be stationary except for the forearms. This is the starting position.	1
7557	320	Rotate one wrist at a time in an upward motion to bring the weight up to the bar by rolling the rope around the roller.	2
7558	320	Once the weight has reached the bar, slowly begin to lower the weight back down by rotating the wrist in a downward motion until the weight reaches the starting position.	3
7559	320	Repeat for the prescribed amount of repetitions in your program.	4
7563	322	The yoke is usually done with a yoke apparatus, but is sometimes seen with refrigerators or other heavy objects.	0
7564	322	Begin by racking the apparatus across the back of the shoulders. With your head looking forward and back arched, lift the yoke by driving through the heels.	1
7565	322	Begin walking as quickly as possible using short, quick steps. You may hold the side posts of the yoke to help steady it and hold it in position. Continue for the given distance as fast as possible, usually 75-100 feet.	2
7566	323	Lie down on the floor and secure your feet. Your legs should be bent at the knees.	0
7567	323	Place your hands behind or to the side of your head. You will begin with your back on the ground. This will be your starting position.	1
7568	323	Flex your hips and spine to raise your torso toward your knees.	2
7569	323	At the top of the contraction your torso should be perpendicular to the ground. Reverse the motion, going only  of the way down.	3
7570	323	Repeat for the recommended amount of repetitions.	4
7571	325	Assume a comfortable stance with one foot slightly in front of the other.	0
7572	325	Begin by pushing off with the front leg, driving the opposite knee forward and as high as possible before landing. Attempt to cover as much distance to each side with each bound.	1
7573	325	It may help to use a line on the ground to guage distance from side to side.	2
7574	325	Repeat the sequence with the other leg.	3
7575	326	Anchor a band around a solid post or other object.	0
7576	326	Stand with your left side to the post, and put your right foot through the band, getting it around the ankle.	1
7577	326	Stand up straight and hold onto the post if needed. This will be your starting position.	2
7578	326	Keeping the knee straight, raise your right legs out to the side as far as you can.	3
7579	326	Return to the starting position and repeat for the desired rep count.	4
7580	326	Switch sides.	5
7581	327	Assume a plank position on the ground. You should be supporting your bodyweight on your toes and forearms, keeping your torso straight. Your forearms should be shoulder-width apart. This will be your starting position.	0
7582	327	Pressing your palms firmly into the ground, extend through the elbows to raise your body from the ground. Keep your torso rigid as you perform the movement.	1
7583	327	Slowly lower your forearms back to the ground by allowing the elbows to flex.	2
7584	327	Repeat.	3
7585	328	Begin by lying on your back on the ground. Your legs should be straight and your arms at your side. This will be your starting position.	0
7586	328	To perform the movement, tuck the knees toward your chest by flexing the hips and knees. Following this, extend your legs directly above you so that they are perpendicular to the ground. Rotate and elevate your pelvis to raise your glutes from the floor.	1
7587	328	After a brief pause, return to the starting position.	2
7588	329	You will need several boxes lined up about 8 feet apart.	0
7589	329	Begin facing the first box with one leg slightly behind the other.	1
7590	329	Drive off the back leg, attempting to gain as much height with the hips as possible.	2
7591	329	Immediately upon landing on the box, drive the other leg forward and upward to gain height and distance, leaping from the box. Land between the first two boxes with the same leg that landed on the first box.	3
7592	329	Then, step to the next box and repeat.	4
7593	333	Stand with your torso upright holding two dumbbells in your hands by your sides. This will be your starting position.	0
7594	333	Step forward with your right leg around 2 feet or so from the foot being left stationary behind and lower your upper body down, while keeping the torso upright and maintaining balance. Inhale as you go down. Note: As in the other exercises, do not allow your knee to go forward beyond your toes as you come down, as this will put undue stress on the knee joint. Make sure that you keep your front shin perpendicular to the ground.	1
7595	333	Using mainly the heel of your foot, push up and go back to the starting position as you exhale.	2
7596	333	Repeat the movement for the recommended amount of repetitions and then perform with the left leg.	3
7602	337	Adjust the j-hooks so they are at the appropriate height to rack the bar. For this exercise, drape the chains directly over the end of the bar, trying to keep the ends away from the plates.	0
7603	337	Begin lying on the floor with your head near the end of a power rack. Keeping your shoulder blades pulled together, pull the bar off of the hooks.	1
7604	337	Lower the bar towards the bottom of your chest or upper stomach, squeezing the bar and attempting to pull it apart as you do so. Ensure that you tuck your elbows throughout the movement. Lower the bar until your upper arm contacts the ground and pause, preventing any slamming or bouncing of the weight.	2
7605	337	Press the bar back up as fast as you can, keeping the bar, your wrists, and elbows in line as you do so.	3
7606	338	Utilize a heavy bag for this exercise. Assume an upright stance next to the bag, with your feet staggered, fairly wide apart. Place your hand on the bag at about chest height. This will be your starting position.	0
7607	338	Begin by twisting at the waist, pushing the bag forward as hard as possible. Perform this move quickly, pushing the bag away from your body.	1
7608	338	Receive the bag as it swings back by reversing these steps.	2
7609	340	Place a kettlebell on the ground between your feet. Position your feet in a wide stance, and grasp the kettlebell with two hands. Set your hips back as far as possible, with your knees bent. Keep your chest and head up. This will be your starting position.	0
7610	340	Begin by extending the hips and knees, simultaneously pulling the kettlebell to your shoulders, raising your elbows as you do so. Reverse the motion to return to the starting position.	1
7611	343	Position a number of cones in a row several feet apart.	0
7612	343	Stand next to the end of the cones, facing 90 degrees to the direction of travel. This will be your starting position.	1
7613	343	Begin the jump by dipping with the knees to initiate a stretch reflex, and immediately reverse direction to push off the ground, jumping up and sideways over the cone.	2
7614	343	Use your legs to absorb impact upon landing, and rebound into the next jump, continuing down the row of cones.	3
7619	345	Lie on your stomach with your arms out to your sides. This will be your starting position.	0
7620	345	Using your lower back muscles, extend your spine lifting your chest off of the ground. Do not use your arms to push yourself up. Keep your head up during the movement. Repeat for 10-20 repetitions.	1
7621	346	Stand with your torso upright holding a kettlebell in your right hand. This will be your starting position.	0
7622	346	Step forward with your left foot and lower your upper body down by flexing the hip and the knee, keeping the torso upright. Lower your back knee until it nearly touches the ground.	1
7623	346	As you lunge, pass the kettlebell under your front leg to your opposite hand.	2
7624	346	Pressing through the heel of your foot, return to the starting position.	3
7625	346	Repeat the movement for the recommended amount of repetitions, alternating legs.	4
7626	350	Secure your feet and lay back on the floor. Your knees should be bent. Hold a weight with both hands to your chest. This will be your starting position.	0
7627	350	Initiate the movement by flexing the hips and spine to raise your torso up from the ground.	1
7597	579	Lie on an exercise mat or a flat bench with your legs off the end.	0
7615	598	Lie on an exercise mat with your legs extended and your hands either palms facing down next to you or under your glutes. Tip: My preference is with the hands next to me. This will be your starting position.	0
7616	598	Bend your knees and pull your upper thighs into your midsection as you breathe out. Continue the motion until your knees are around chest level. Contract your abs as you execute this movement and hold for a second at the top. Tip: As you perform the motion, the lower legs (calves) should always remain parallel to the floor.	1
7617	598	Return to the starting position as you inhale.	2
7628	350	As you move up, press the weight up so that it is above your head at the top of the movement.	2
7629	350	Return the weight to your chest as you reverse the sit-up motion, ensuring not to go all the way down to the floor.	3
7630	342	Start by kneeling on a mat with your palms flat and your fingers pointing back toward your knees.	0
7631	342	Slowly lean back keeping your palms flat on the floor until you feel a stretch in your wrists and forearms. Hold for 20-30 seconds.	1
7632	347	Stand so your feet are shoulder width apart and your hands are on your hips.	0
7633	347	Twist at your waist until you feel a stretch. Hold for 10 to 15 seconds, then twist to the other side.	1
7642	359	Put a bench in front of a low pulley machine that has a barbell or EZ Curl attachment on it.	0
7643	359	Move the bench far enough away so that when you bring the handle to the top of your thighs tension is created on the cable due to the weight stack being moved up.	1
7644	359	Now hold the handle with both hands, palms up, using a shoulder-width grip.	2
7645	359	Step back and sit on the bench with your feet about shoulder width apart, firmly on the floor.	3
7646	359	Lean forward and place the forearms on your thighs with the back of your wrists over your knees. This will be your starting position.	4
7647	359	Lower the bar as far as possible, while inhaling and keeping a tight grip.	5
7648	359	Now curl the bar up as high as possible while contracting the forearms. Tip: Only the wrist should move; not the forearms.	6
7649	359	After a second contraction at the top go back to the starting position as you inhale.	7
7650	359	Repeat for the recommended amount of repetitions.	8
7651	361	Stand next to a chair, which you may hold onto as a support. Stand on one leg. This will be your starting position.	0
7652	361	Keeping your leg straight, raise it as far out to the side as possible, and swing it back down, allowing it to cross the opposite leg.	1
7653	361	Repeat this swinging motion 5-10 times, increasing the range of motion as you do so.	2
7654	356	It's easiest to get into this stretch if you start standing up, put one leg behind you, and slowly lower your torso down to the floor.	0
7655	356	Keep the front heel on the floor (if it lifts up, scoot your other leg further back).	1
7656	356	Place your hands on either side of your front leg. To get more out of this stretch, push your butt up toward the ceiling, and then gradually lower it back toward the floor. You'll Stretch the hip flexor of the back leg and the hamstring and buttocks of the front.	2
7657	363	For this exercise anchor a band to the ground. We used an incline bench and anchored the band to the base, standing over the bench. Alternatively, this could be performed standing on the band.	0
7658	363	To begin, pull the band behind your head, holding it with a pronated grip and your elbows up. This will be your starting position.	1
7659	363	To perform the movement, extend through the elbow to to straighten your arms, ensuring that you keep your upper arm in place.	2
7660	363	Pause, and then return to the starting position.	3
7664	367	Place a loaded barbell on the end of a bench. Standing on the bench behind the bar, take a medium, pronated grip. Stand with your hips back and chest up, maintaining a neutral spine. This will be your starting position.	0
7665	367	Row the bar to your torso by retracting the shoulder blades and flexing the elbows. Use a controlled movement with no jerking.	1
7666	367	After a brief pause, slowly return the bar to the starting position, ensuring to go all the way down.	2
7667	368	Sit down on a pull-down machine with a wide bar attached to the top pulley. Adjust the knee pad of the machine to fit your height. These pads will prevent your body from being raised by the resistance attached to the bar.	0
7668	368	Grab the pull-down bar with the palms facing your torso (a supinated grip). Make sure that the hands are placed closer than the shoulder width.	1
7669	368	As you have both arms extended in front of you holding the bar at the chosen grip width, bring your torso back around 30 degrees or so while creating a curvature on your lower back and sticking your chest out. This is your starting position.	2
7670	368	As you breathe out, pull the bar down until it touches your upper chest by drawing the shoulders and the upper arms down and back. Tip: Concentrate on squeezing the back muscles once you reach the fully contracted position and keep the elbows close to your body. The upper torso should remain stationary as your bring the bar to you and only the arms should move. The forearms should do no other work other than hold the bar.	3
7671	368	After a second on the contracted position, while breathing in, slowly bring the bar back to the starting position when your arms are fully extended and the lats are fully stretched.	4
7672	368	Repeat this motion for the prescribed amount of repetitions.	5
7640	613	After a second pause, go back to the starting position as you inhale.	2
7661	623	Stand facing a box or bench of an appropriate height with your feet together. This will be your starting position.	0
7662	623	Begin the movement by stepping up, putting your left foot on the top of the bench. Extend through the hip and knee of your front leg to stand up on the box. As you stand on the box with your left leg, flex your right knee and hip, bringing your knee as high as you can.	1
7663	623	Reverse this motion to step down off the box, and then repeat the sequence on the opposite leg.	2
7673	365	Start by standing with your back about two to three feet away from a bench or step.	0
7674	365	Lift one leg behind you and rest your foot on the step,either on your instep or the ball of your foot, whichever you find most comfortable.	1
7675	365	Keep your supporting knee slightly bent and avoid letting that knee extend out beyond your toes. Switch sides.	2
6933	131	Lie flat on your back with your feet flat on the ground, or resting on a bench with your knees bent at a 90 degree angle. If you are resting your feet on a bench, place them three to four inches apart and point your toes inward so they touch.	0
6934	131	Now place your hands lightly on either side of your head keeping your elbows in. Tip: Don't lock your fingers behind your head.	1
6935	131	While pushing the small of your back down in the floor to better isolate your abdominal muscles, begin to roll your shoulders off the floor.	2
6936	131	Continue to push down as hard as you can with your lower back as you contract your abdominals and exhale. Your shoulders should come up off the floor only about four inches, and your lower back should remain on the floor. At the top of the movement, contract your abdominals hard and keep the contraction for a second. Tip: Focus on slow, controlled movement - don't cheat yourself by using momentum.	3
6937	131	After the one second contraction, begin to come down slowly again to the starting position as you inhale.	4
6938	131	Repeat for the recommended amount of repetitions.	5
7598	579	Place your hands either under your glutes with your palms down or by the sides holding on to the bench (or with palms down by the side on an exercise mat). Also extend your legs straight out. This will be your starting position.	1
7599	579	Bend your knees and pull your upper thighs into your midsection as you breathe out. Continue this movement until your knees are near your chest. Hold the contracted position for a second.	2
7600	579	As you breathe in, slowly return to the starting position.	3
7601	579	Repeat for the recommended amount of repetitions.	4
7020	670	This exercise stretches the fascia of the muscles in the feet. Start off seated with your shoes removed. Using a foot roller or a similar object, such as a small section of pvc pipe, place your foot against the roller across the arch of your foot. This will be your starting position.	0
7021	670	Press down firmly, rolling across the arch of your foot. Hold for 10-30 seconds, and then switch feet.	1
7049	672	Roll over the foam from below the hip to above the back of the knee, pausing at points of tension for 10-30 seconds. Repeat for the other leg.	2
7618	598	Repeat for the recommended amount of repetitions.	3
6637	216	Start out by lying on your right side with your legs lying on top of each other. Make sure your knees are bent a little bit.	0
6638	216	Place your left hand behind your head.	1
6639	216	Once you are in this set position, begin by moving your left elbow up as you would perform a normal crunch except this time the main emphasis is on your obliques.	2
6640	216	Crunch as high as you can, hold the contraction for a second and then slowly drop back down into the starting position.	3
6641	216	Remember to breathe in during the eccentric (lowering) part of the exercise and to breathe out during the concentric (elevation) part of the exercise.	4
6611	684	Lay on your side, supporting your weight on your forearm and on a foam roller placed on the outside of your lower leg. Your upper leg can either be on top of your lower leg, or you can cross it in front of you. This will be your starting position.	0
6612	684	Raise your hips off of the ground and begin to roll from below the knee to above the ankle on the side of your leg, pausing at points of tension for 10-30 seconds. Repeat on the other leg.	1
7525	624	Start by placing the middle of the V-bar in the middle of the pull-up bar (assuming that the pull-up station you are using does not have neutral grip handles). The V-Bar handles will be facing down so that you can hang from the pull-up bar through the use of the handles.	0
7526	624	Once you securely place the V-bar, take a hold of the bar from each side and hang from it. Stick your chest out and lean yourself back slightly in order to better engage the lats. This will be your starting position.	1
7527	624	Using your lats, pull your torso up while leaning your head back slightly so that you do not hit yourself with the chin-up bar. Continue until your chest nearly touches the V-bar. Exhale as you execute this motion.	2
7529	624	Repeat for the prescribed number of repetitions.	4
7560	320	Hold a barbell with both hands and your palms facing down; hands spaced about shoulder width. This will be your starting position.	0
7561	320	Alternating between each of your hands, perform the movement by extending the wrist as though you were rolling up a newspaper. Continue alternating back and forth until failure.	1
7562	320	Reverse the motion by flexing the wrist, rolling the opposite direction. Continue the alternating motion until failure.	2
6594	389	To begin, step onto the treadmill and select the desired option from the menu. Most treadmills have a manual setting, or you can select a program to run. Typically, you can enter your age and weight to estimate the amount of calories burned during exercise. Elevation can be adjusted to change the intensity of the workout.	0
6595	389	Treadmills offer convenience, cardiovascular benefits, and usually have less impact than running outside. A 150 lb person will burn over 450 calories running 8 miles per hour for 30 minutes. Maintain proper posture as you run, and only hold onto the handles when necessary, such as when dismounting or checking your heart rate.	1
7281	16	Lie on the floor face down and place your hands closer than shoulder width for a close hand position. Make sure that you are holding your torso up at arms' length.	0
7282	16	Lower yourself until your chest almost touches the floor as you inhale.	1
7283	16	Using your triceps and some of your pectoral muscles, press your upper body back up to the starting position and squeeze your chest. Breathe out as you perform this step.	2
7285	16	Lie on the floor face down and place your hands about 36 inches apart from each other holding your torso up at arms length.	0
7286	16	Place your toes on top of a flat bench. This will allow your body to be elevated. Note: The higher the elevation of the flat bench, the higher the resistance of the exercise is.	1
7287	16	Lower yourself until your chest almost touches the floor as you inhale.	2
7288	16	Using your pectoral muscles, press your upper body back up to the starting position and squeeze your chest. Breathe out as you perform this step.	3
7289	16	After a second pause at the contracted position, repeat the movement for the prescribed amount of repetitions.	4
6888	524	Stand facing a wall from several feet away. Stagger your stance, placing one foot forward.	0
6889	524	Lean forward and rest your hands on the wall, keeping your heel, hip and head in a straight line.	1
6890	524	Attempt to keep your heel on the ground. Hold for 10-20 seconds and then switch sides.	2
7243	512	Begin in a pushup position, with your weight supported by your hands and toes. Flexing the knee and hip, bring one leg until the knee is approximately under the hip. This will be your starting position.	0
7244	512	Explosively reverse the positions of your legs, extending the bent leg until the leg is straight and supported by the toe, and bringing the other foot up with the hip and knee flexed. Repeat in an alternating fashion for 20-30 seconds.	1
7324	536	To begin, lie down on an incline bench with the chest and stomach pressing against the incline. Have the dumbbells in each hand with the palms facing each other (neutral grip).	0
7325	536	Extend the arms in front of you so that they are perpendicular to the angle of the bench. The legs should be stationary while applying pressure with the ball of your toes. This is the starting position.	1
7326	536	Maintaining the slight bend of the elbows, move the weights out and away from each other (to the side) in an arc motion while exhaling. Tip: Try to squeeze your shoulder blades together to get the best results from this exercise.	2
7327	536	The arms should be elevated until they are parallel to the floor.	3
7328	536	Feel the contraction and slowly lower the weights back down to the starting position while inhaling.	4
7329	536	Repeat for the recommended amount of repetitions.	5
7333	536	To begin, lie down on an incline bench set at a 30-degree angle with the chest and stomach pressing against the incline.	0
7334	536	Have the dumbbells in each hand with the palms facing down to the floor. Your arms should be in front of you so that they are perpendicular to the angle of the bench. Tip: Your elbows should have a slight bend. The legs should be stationary while applying pressure with the ball of your toes (your heels should not be touching the floor). This is the starting position.	1
7335	536	Maintaining the slight bend of the elbows, move the weights out and away from each other in an arc motion while exhaling.	2
7336	536	As you lift the weight, your wrist should externally rotate by 90-degrees so that you go from a palms down (pronated) grip to a palms facing each other (neutral) grip. Tip: Try to squeeze your shoulder blades together to get the best results from this exercise.	3
7337	536	The arms should be elevated until they are level with the head.	4
7338	536	Feel the contraction and slowly lower the weights back down to the starting position while inhaling.	5
7339	536	Repeat for the recommended amount of repetitions.	6
6699	383	Hold an end of the rope in each hand. Position the rope behind you on the ground. Raise your arms up and turn the rope over your head bringing it down in front of you. When it reaches the ground, jump over it. Find a good turning pace that can be maintained. Different speeds and techniques can be used to introduce variation.	0
6700	383	Rope jumping is exciting, challenges your coordination, and requires a lot of energy. A 150 lb person will burn about 350 calories jumping rope for 30 minutes, compared to over 450 calories running.	1
7638	613	Sit on a bench with the legs stretched out in front of you slightly below parallel and your arms holding on to the sides of the bench. Your torso should be leaning backwards around a 45-degree angle from the bench. This will be your starting position.	0
7639	613	Bring the knees in toward you as you move your torso closer to them at the same time. Breathe out as you perform this movement.	1
7641	613	Repeat for the recommended amount of repetitions.	3
6625	692	In a seated position with your legs extended, have your partner stand behind you. Now, lean forward as your partner braces your shoulders with their hands. This will be your starting position.	0
6626	692	Attempt to push your torso back for 10-20 seconds, as your partner prevents any actual movement of your torso.	1
6627	692	Now relax your muscles as your partner increases the stretch by gently pushing your torso forward for 10-20 seconds.	2
7359	502	Grip a ring in each hand, and then take a small jump to help you get into the starting position with your arms locked out.	0
7360	502	Begin by flexing the elbow, lowering your body until your arms break 90 degrees. Avoid swinging, and maintain good posture throughout the descent.	1
7361	502	Reverse the motion by extending the elbow, pushing yourself back up into the starting position.	2
7362	502	Repeat for the desired number of repetitions.	3
101	712	Start in a standing position with feet shoulder-width apart	0
102	712	Drop into a squat position and place hands on floor	1
103	712	Jump feet back to plank position	2
104	712	Perform a push-up	3
105	712	Jump feet forward to hands	4
106	712	Explode upward into a broad jump	5
107	712	Land softly with knees bent	6
108	712	Immediately return to plank position	7
109	712	Perform next push-up	8
110	712	Repeat for prescribed reps	9
111	713	Set foot straps securely	0
112	713	Maintain tall posture throughout	1
113	713	Drive through each stroke with power	2
114	713	Keep core engaged and body straight	3
115	713	Use full range of motion on pull	4
116	713	Control of return stroke	5
117	713	Focus on breathing rhythm	6
118	714	Lie on back with arms extended overhead	0
119	714	Keep legs straight and together	1
120	714	Engage core throughout movement	2
121	714	Reach toes toward hands	3
122	714	Lift shoulders off ground	4
123	714	Lower with control	5
124	714	Touch toes to floor on each rep	6
125	714	Avoid swinging legs for momentum	7
126	715	Lie on back with knees bent at 90 degrees	0
127	715	Place hands behind head or crossed over chest	1
128	715	Engage core and lift shoulder blades	2
129	715	Curl up until elbows touch knees or thighs	3
130	715	Pause at top for full contraction	4
131	715	Lower with control	5
132	715	Keep feet flat on floor	6
133	715	Exhale on way up, inhale on way down	7
134	716	Stand with feet shoulder-width apart	0
135	716	Hold sandbag securely at shoulder height or in front rack	1
136	716	Step forward into lunge position	2
137	716	Keep front knee behind toes	3
138	716	Lower until back knee nearly touches ground	4
139	716	Drive through front heel to return	5
140	716	Keep torso upright throughout	6
141	716	Maintain stability of sandbag	7
142	716	Alternate legs for prescribed reps	8
143	717	Stand tall with feet shoulder-width apart	0
144	717	Step forward into lunge position	1
145	717	Keep front knee behind toes	2
146	717	Lower until back knee nearly touches ground	3
147	717	Drive through front heel to return	4
148	717	Keep torso upright and core engaged	5
149	717	Maintain 90-degree knee angles	6
150	717	Alternate legs for prescribed reps	7
151	712	Start in a standing position with feet shoulder-width apart	0
152	712	Drop into a squat position and place hands on floor	1
153	712	Jump feet back to plank position	2
154	712	Perform a push-up	3
155	712	Jump feet forward to hands	4
156	712	Explode upward into a broad jump	5
157	712	Land softly with knees bent	6
158	712	Immediately return to plank position	7
159	712	Perform next push-up	8
160	712	Repeat for prescribed reps	9
161	713	Set foot straps securely	0
162	713	Maintain tall posture throughout	1
163	713	Drive through each stroke with power	2
164	713	Keep core engaged and body straight	3
165	713	Use full range of motion on pull	4
166	713	Control of return stroke	5
167	713	Focus on breathing rhythm	6
168	714	Lie on back with arms extended overhead	0
169	714	Keep legs straight and together	1
170	714	Engage core throughout movement	2
171	714	Reach toes toward hands	3
172	714	Lift shoulders off ground	4
173	714	Lower with control	5
174	714	Touch toes to floor on each rep	6
175	714	Avoid swinging legs for momentum	7
176	715	Lie on back with knees bent at 90 degrees	0
177	715	Place hands behind head or crossed over chest	1
178	715	Engage core and lift shoulder blades	2
179	715	Curl up until elbows touch knees or thighs	3
180	715	Pause at top for full contraction	4
181	715	Lower with control	5
182	715	Keep feet flat on floor	6
183	715	Exhale on way up, inhale on way down	7
184	716	Stand with feet shoulder-width apart	0
185	716	Hold sandbag securely at shoulder height or in front rack	1
186	716	Step forward into lunge position	2
187	716	Keep front knee behind toes	3
188	716	Lower until back knee nearly touches ground	4
189	716	Drive through front heel to return	5
190	716	Keep torso upright throughout	6
191	716	Maintain stability of sandbag	7
192	716	Alternate legs for prescribed reps	8
193	717	Stand tall with feet shoulder-width apart	0
194	717	Step forward into lunge position	1
195	717	Keep front knee behind toes	2
196	717	Lower until back knee nearly touches ground	3
197	717	Drive through front heel to return	4
198	717	Keep torso upright and core engaged	5
199	717	Maintain 90-degree knee angles	6
200	717	Alternate legs for prescribed reps	7
\.


--
-- Data for Name: movement_equipment; Type: TABLE DATA; Schema: public; Owner: jacked
--

COPY public.movement_equipment (movement_id, equipment_id) FROM stdin;
507	211
508	223
509	223
510	225
511	225
512	211
515	223
521	211
522	213
523	211
524	211
525	211
526	211
527	211
528	211
529	211
531	211
533	211
534	211
535	223
536	225
540	211
541	211
542	211
543	211
544	222
545	211
72	211
75	213
76	211
123	211
227	211
228	211
231	214
245	214
259	214
269	211
40	215
40	216
41	217
42	218
270	211
294	211
297	211
299	211
305	211
309	211
319	211
324	211
330	213
332	213
334	211
335	211
339	213
348	213
349	211
358	211
369	211
370	211
371	211
43	219
45	219
46	221
235	222
341	211
152	212
180	212
289	212
296	212
101	211
103	215
104	215
109	215
1	223
1	224
2	223
2	224
5	225
5	223
6	225
7	223
8	223
8	225
9	225
9	222
10	223
10	225
11	223
12	222
13	223
13	226
14	223
14	225
14	226
15	225
15	226
17	227
18	223
19	225
22	223
23	225
23	215
23	222
24	215
25	228
26	217
27	217
28	215
29	228
29	217
59	229
60	217
60	228
61	230
64	231
127	213
65	222
65	225
34	225
34	222
34	232
35	225
35	222
36	225
36	222
36	223
63	233
67	212
70	222
222	222
71	211
73	211
77	225
78	213
79	213
74	211
81	213
84	225
84	226
85	223
86	223
87	223
88	213
89	213
90	223
97	222
95	235
96	215
99	223
98	214
93	213
94	212
225	211
102	215
105	215
106	215
107	215
108	215
110	215
111	215
112	215
113	215
116	214
117	223
118	211
124	213
125	235
128	211
120	213
122	237
130	213
134	226
135	225
136	211
137	211
138	212
119	221
121	221
4	211
5	211
141	222
142	237
143	225
144	225
145	225
146	225
147	225
148	225
149	235
149	226
151	211
150	211
153	222
226	213
154	211
155	223
50	215
50	216
156	211
158	211
372	212
131	211
670	213
216	211
684	214
16	211
32	223
186	211
400	212
159	213
160	211
161	211
162	211
165	237
166	211
167	213
223	225
51	212
51	225
168	213
170	214
171	211
52	212
53	212
172	215
173	225
174	225
175	225
177	211
178	211
179	211
181	213
182	222
176	211
183	222
187	211
188	211
184	222
185	222
186	222
189	213
190	211
191	215
192	223
193	223
194	214
195	212
196	211
197	211
224	215
198	213
199	213
200	211
201	215
203	235
202	213
58	230
204	211
66	211
210	212
364	211
68	214
209	211
401	238
47	225
47	223
47	215
48	225
48	215
49	225
49	215
211	213
214	211
31	223
400	240
406	222
408	242
411	228
412	243
331	211
215	213
230	223
232	213
233	213
234	213
236	211
241	223
243	211
244	237
246	213
248	223
251	235
252	211
249	212
255	223
256	212
257	212
258	213
261	213
265	211
266	213
268	223
279	211
267	211
272	213
273	215
274	213
275	215
276	223
277	213
278	211
281	213
282	213
283	213
284	212
285	212
286	225
287	211
308	213
280	213
290	215
291	215
292	213
293	211
298	225
303	213
304	213
306	212
307	212
310	211
312	237
314	213
315	223
317	211
320	213
322	213
323	211
325	211
327	211
328	211
329	213
333	225
337	223
338	213
340	222
343	213
345	211
346	222
350	213
342	211
347	211
359	215
360	211
361	211
356	211
367	223
368	215
365	213
80	216
83	216
164	216
212	216
326	216
363	216
401	225
250	221
295	221
300	221
301	221
302	221
313	221
402	217
407	217
6	211
9	211
17	211
20	211
25	211
29	211
37	211
38	211
39	211
44	211
51	211
54	211
55	211
56	211
57	211
58	211
59	211
60	211
61	211
62	211
579	211
672	214
598	211
623	211
624	211
320	223
627	223
628	223
629	223
631	223
632	223
633	223
634	223
635	223
637	223
638	223
639	223
640	223
641	223
642	223
643	223
644	223
645	223
646	223
647	223
648	223
649	223
654	223
655	223
656	223
657	223
658	223
659	223
662	213
666	211
667	211
668	211
669	211
671	211
673	213
676	211
678	211
680	213
682	211
683	213
685	213
687	213
689	213
690	211
691	211
692	213
693	211
694	211
695	211
696	211
697	211
698	211
699	211
700	211
701	213
703	213
704	211
705	211
706	211
708	211
711	211
563	211
564	211
565	211
568	211
569	211
571	211
572	211
573	211
577	211
578	211
580	211
581	211
582	211
583	211
585	211
586	211
587	211
589	211
590	211
592	211
593	211
594	211
595	211
596	211
600	211
602	211
603	211
605	211
608	211
610	211
611	211
612	211
613	211
614	211
615	211
616	211
618	211
620	211
621	211
622	211
625	211
674	214
679	214
707	237
30	223
33	223
247	223
316	223
546	223
27	211
26	211
491	225
491	222
131	211
131	211
389	212
245	214
231	214
369	211
75	213
116	214
98	214
194	214
16	211
16	211
16	211
16	211
16	211
16	211
635	223
524	211
512	211
536	225
536	225
383	213
8	223
613	211
692	211
614	211
501	211
502	213
708	211
712	211
713	212
714	211
715	211
717	211
712	211
713	212
714	211
715	211
717	211
\.


--
-- Data for Name: movement_equipment_backup_20260301; Type: TABLE DATA; Schema: public; Owner: jacked
--

COPY public.movement_equipment_backup_20260301 (movement_id, equipment_id) FROM stdin;
507	211
508	223
509	223
510	225
511	225
512	211
515	223
521	211
522	213
523	211
524	211
525	211
526	211
527	211
528	211
529	211
531	211
533	211
534	211
535	223
536	225
540	211
541	211
542	211
543	211
544	222
545	211
72	211
75	213
76	211
123	211
227	211
228	211
231	214
245	214
259	214
269	211
40	215
40	216
41	217
42	218
270	211
294	211
297	211
299	211
305	211
309	211
319	211
324	211
330	213
332	213
334	211
335	211
339	213
348	213
349	211
358	211
369	211
370	211
371	211
43	219
45	219
46	221
235	222
341	211
152	212
180	212
289	212
296	212
101	211
103	215
104	215
109	215
1	223
1	224
2	223
2	224
5	225
5	223
6	225
7	223
8	223
8	225
9	225
9	222
10	223
10	225
11	223
12	222
13	223
13	226
14	223
14	225
14	226
15	225
15	226
17	227
18	223
19	225
22	223
23	225
23	215
23	222
24	215
25	228
26	217
27	217
28	215
29	228
29	217
59	229
60	217
60	228
61	230
64	231
127	213
65	222
65	225
34	225
34	222
34	232
35	225
35	222
36	225
36	222
36	223
63	233
67	212
70	222
222	222
71	211
73	211
77	225
78	213
79	213
74	211
81	213
84	225
84	226
85	223
86	223
87	223
88	213
89	213
90	223
97	222
95	235
96	215
99	223
98	214
93	213
94	212
225	211
102	215
105	215
106	215
107	215
108	215
110	215
111	215
112	215
113	215
116	214
117	223
118	211
124	213
125	235
128	211
120	213
122	237
130	213
134	226
135	225
136	211
137	211
138	212
119	221
121	221
4	211
5	211
141	222
142	237
143	225
144	225
145	225
146	225
147	225
148	225
149	235
149	226
151	211
150	211
153	222
226	213
154	211
155	223
50	215
50	216
156	211
158	211
372	212
131	211
670	213
216	211
684	214
16	211
32	223
186	211
400	212
159	213
160	211
161	211
162	211
165	237
166	211
167	213
223	225
51	212
51	225
168	213
170	214
171	211
52	212
53	212
172	215
173	225
174	225
175	225
177	211
178	211
179	211
181	213
182	222
176	211
183	222
187	211
188	211
184	222
185	222
186	222
189	213
190	211
191	215
192	223
193	223
194	214
195	212
196	211
197	211
224	215
198	213
199	213
200	211
201	215
203	235
202	213
58	230
204	211
66	211
210	212
364	211
68	214
209	211
401	238
47	225
47	223
47	215
48	225
48	215
49	225
49	215
211	213
214	211
31	223
400	240
406	222
408	242
411	228
412	243
331	211
215	213
230	223
232	213
233	213
234	213
236	211
241	223
243	211
244	237
246	213
248	223
251	235
252	211
249	212
255	223
256	212
257	212
258	213
261	213
265	211
266	213
268	223
279	211
267	211
272	213
273	215
274	213
275	215
276	223
277	213
278	211
281	213
282	213
283	213
284	212
285	212
286	225
287	211
308	213
280	213
290	215
291	215
292	213
293	211
298	225
303	213
304	213
306	212
307	212
310	211
312	237
314	213
315	223
317	211
320	213
322	213
323	211
325	211
327	211
328	211
329	213
333	225
337	223
338	213
340	222
343	213
345	211
346	222
350	213
342	211
347	211
359	215
360	211
361	211
356	211
367	223
368	215
365	213
80	216
83	216
164	216
212	216
326	216
363	216
401	225
250	221
295	221
300	221
301	221
302	221
313	221
402	217
407	217
6	211
9	211
17	211
20	211
25	211
29	211
37	211
38	211
39	211
44	211
51	211
54	211
55	211
56	211
57	211
58	211
59	211
60	211
61	211
62	211
579	211
672	214
598	211
623	211
624	211
320	223
627	223
628	223
629	223
631	223
632	223
633	223
634	223
635	223
637	223
638	223
639	223
640	223
641	223
642	223
643	223
644	223
645	223
646	223
647	223
648	223
649	223
654	223
655	223
656	223
657	223
658	223
659	223
662	213
666	211
667	211
668	211
669	211
671	211
673	213
676	211
678	211
680	213
682	211
683	213
685	213
687	213
689	213
690	211
691	211
692	213
693	211
694	211
695	211
696	211
697	211
698	211
699	211
700	211
701	213
703	213
704	211
705	211
706	211
708	211
711	211
563	211
564	211
565	211
568	211
569	211
571	211
572	211
573	211
577	211
578	211
580	211
581	211
582	211
583	211
585	211
586	211
587	211
589	211
590	211
592	211
593	211
594	211
595	211
596	211
600	211
602	211
603	211
605	211
608	211
610	211
611	211
612	211
613	211
614	211
615	211
616	211
618	211
620	211
621	211
622	211
625	211
674	214
679	214
707	237
30	223
33	223
247	223
316	223
546	223
27	211
26	211
491	225
491	222
131	211
131	211
389	212
245	214
231	214
369	211
75	213
116	214
98	214
194	214
16	211
16	211
16	211
16	211
16	211
16	211
635	223
524	211
512	211
536	225
536	225
383	213
8	223
613	211
692	211
614	211
501	211
502	213
708	211
\.


--
-- Data for Name: movement_muscle_map; Type: TABLE DATA; Schema: public; Owner: jacked
--

COPY public.movement_muscle_map (id, movement_id, muscle_id, role, magnitude) FROM stdin;
600	76	45	SECONDARY	1
601	123	41	SECONDARY	1
602	123	57	SECONDARY	1
603	227	40	SECONDARY	1
604	227	54	SECONDARY	1
605	259	45	SECONDARY	1
606	269	43	SECONDARY	1
607	269	57	SECONDARY	1
608	40	53	SECONDARY	1
609	41	55	SECONDARY	1
610	42	44	SECONDARY	1
611	42	47	SECONDARY	1
612	270	56	SECONDARY	1
614	294	42	SECONDARY	1
615	299	41	SECONDARY	1
616	299	40	SECONDARY	1
617	305	56	SECONDARY	1
618	305	42	SECONDARY	1
622	324	39	SECONDARY	1
623	330	56	SECONDARY	1
624	332	49	SECONDARY	1
625	332	43	SECONDARY	1
626	335	57	SECONDARY	1
627	358	43	SECONDARY	1
628	369	54	SECONDARY	1
629	369	57	SECONDARY	1
630	370	57	SECONDARY	1
631	371	42	SECONDARY	1
632	371	41	SECONDARY	1
633	371	39	SECONDARY	1
634	43	41	SECONDARY	1
635	43	42	SECONDARY	1
636	44	39	SECONDARY	1
637	44	40	SECONDARY	1
638	45	41	SECONDARY	1
639	45	42	SECONDARY	1
640	46	44	SECONDARY	1
641	46	47	SECONDARY	1
642	235	57	SECONDARY	1
643	235	50	SECONDARY	1
646	341	56	SECONDARY	1
647	341	42	SECONDARY	1
648	341	41	SECONDARY	1
649	341	39	SECONDARY	1
650	152	42	SECONDARY	1
651	152	41	SECONDARY	1
652	152	40	SECONDARY	1
653	180	41	SECONDARY	1
654	180	40	SECONDARY	1
655	289	42	SECONDARY	1
656	289	41	SECONDARY	1
657	289	40	SECONDARY	1
658	296	42	SECONDARY	1
659	296	41	SECONDARY	1
660	296	40	SECONDARY	1
661	101	40	SECONDARY	1
662	104	51	SECONDARY	1
663	104	41	SECONDARY	1
664	104	40	SECONDARY	1
665	104	54	SECONDARY	1
668	1	52	SECONDARY	1
671	2	45	SECONDARY	1
674	4	41	SECONDARY	1
675	4	55	SECONDARY	1
676	4	52	SECONDARY	1
677	5	41	SECONDARY	1
678	5	40	SECONDARY	1
679	6	41	SECONDARY	1
680	6	40	SECONDARY	1
684	7	51	SECONDARY	1
685	8	41	SECONDARY	1
686	8	54	SECONDARY	1
687	9	41	SECONDARY	1
688	9	52	SECONDARY	1
689	10	40	SECONDARY	1
690	11	41	SECONDARY	1
691	11	54	SECONDARY	1
692	12	40	SECONDARY	1
693	12	52	SECONDARY	1
694	12	44	SECONDARY	1
697	14	47	SECONDARY	1
698	14	50	SECONDARY	1
699	15	47	SECONDARY	1
700	15	50	SECONDARY	1
701	16	47	SECONDARY	1
702	16	50	SECONDARY	1
703	16	52	SECONDARY	1
704	17	50	SECONDARY	1
705	17	47	SECONDARY	1
708	18	52	SECONDARY	1
709	19	50	SECONDARY	1
710	19	48	SECONDARY	1
711	20	50	SECONDARY	1
712	20	52	SECONDARY	1
719	23	45	SECONDARY	1
720	23	46	SECONDARY	1
721	23	49	SECONDARY	1
722	24	45	SECONDARY	1
723	24	49	SECONDARY	1
724	25	44	SECONDARY	1
725	25	46	SECONDARY	1
726	25	49	SECONDARY	1
729	26	52	SECONDARY	1
732	28	49	SECONDARY	1
733	28	45	SECONDARY	1
734	29	43	SECONDARY	1
735	29	50	SECONDARY	1
736	29	52	SECONDARY	1
737	37	53	SECONDARY	1
738	37	47	SECONDARY	1
739	38	52	SECONDARY	1
740	38	48	SECONDARY	1
741	39	55	SECONDARY	1
742	59	55	SECONDARY	1
743	59	50	SECONDARY	1
744	60	52	SECONDARY	1
745	60	47	SECONDARY	1
746	61	41	SECONDARY	1
747	64	47	SECONDARY	1
748	64	49	SECONDARY	1
749	127	52	SECONDARY	1
750	127	49	SECONDARY	1
751	127	42	SECONDARY	1
752	127	51	SECONDARY	1
753	127	54	SECONDARY	1
754	127	57	SECONDARY	1
755	127	45	SECONDARY	1
756	65	52	SECONDARY	1
757	65	47	SECONDARY	1
758	65	41	SECONDARY	1
759	62	39	SECONDARY	1
760	62	41	SECONDARY	1
761	62	42	SECONDARY	1
762	34	52	SECONDARY	1
763	34	45	SECONDARY	1
764	34	39	SECONDARY	1
765	35	52	SECONDARY	1
766	35	51	SECONDARY	1
767	35	45	SECONDARY	1
768	36	52	SECONDARY	1
769	36	45	SECONDARY	1
770	63	41	SECONDARY	1
771	63	42	SECONDARY	1
772	63	52	SECONDARY	1
773	70	41	SECONDARY	1
774	70	40	SECONDARY	1
775	70	57	SECONDARY	1
776	222	42	SECONDARY	1
777	222	41	SECONDARY	1
778	222	54	SECONDARY	1
779	222	57	SECONDARY	1
780	77	57	SECONDARY	1
781	78	49	SECONDARY	1
782	78	51	SECONDARY	1
783	78	41	SECONDARY	1
784	78	40	SECONDARY	1
785	78	39	SECONDARY	1
786	79	52	SECONDARY	1
787	79	56	SECONDARY	1
788	79	49	SECONDARY	1
789	79	42	SECONDARY	1
790	79	51	SECONDARY	1
791	79	41	SECONDARY	1
792	79	40	SECONDARY	1
793	79	57	SECONDARY	1
794	79	39	SECONDARY	1
795	79	45	SECONDARY	1
796	80	57	SECONDARY	1
797	80	50	SECONDARY	1
798	81	42	SECONDARY	1
799	81	51	SECONDARY	1
800	81	41	SECONDARY	1
801	81	40	SECONDARY	1
802	81	54	SECONDARY	1
805	83	51	SECONDARY	1
806	84	51	SECONDARY	1
807	85	42	SECONDARY	1
808	85	40	SECONDARY	1
809	87	42	SECONDARY	1
810	87	41	SECONDARY	1
811	87	40	SECONDARY	1
812	87	39	SECONDARY	1
813	88	43	SECONDARY	1
814	88	51	SECONDARY	1
815	89	42	SECONDARY	1
816	89	41	SECONDARY	1
817	89	40	SECONDARY	1
818	90	43	SECONDARY	1
819	90	44	SECONDARY	1
820	90	57	SECONDARY	1
821	90	50	SECONDARY	1
822	97	49	SECONDARY	1
823	97	57	SECONDARY	1
824	95	52	SECONDARY	1
825	95	57	SECONDARY	1
826	95	50	SECONDARY	1
827	99	50	SECONDARY	1
828	93	42	SECONDARY	1
829	93	41	SECONDARY	1
830	93	40	SECONDARY	1
831	94	42	SECONDARY	1
832	94	41	SECONDARY	1
833	94	40	SECONDARY	1
834	225	52	SECONDARY	1
835	225	49	SECONDARY	1
836	225	43	SECONDARY	1
837	102	57	SECONDARY	1
838	110	49	SECONDARY	1
839	110	57	SECONDARY	1
840	117	51	SECONDARY	1
841	389	42	SECONDARY	1
842	389	41	SECONDARY	1
843	389	39	SECONDARY	1
844	118	52	SECONDARY	1
845	118	56	SECONDARY	1
846	118	42	SECONDARY	1
847	118	41	SECONDARY	1
848	118	40	SECONDARY	1
849	118	39	SECONDARY	1
850	119	52	SECONDARY	1
851	119	43	SECONDARY	1
852	119	57	SECONDARY	1
853	121	52	SECONDARY	1
854	121	57	SECONDARY	1
855	121	50	SECONDARY	1
856	124	51	SECONDARY	1
857	124	41	SECONDARY	1
858	124	40	SECONDARY	1
859	124	54	SECONDARY	1
860	124	45	SECONDARY	1
861	124	50	SECONDARY	1
862	125	43	SECONDARY	1
863	125	57	SECONDARY	1
864	120	57	SECONDARY	1
865	130	51	SECONDARY	1
866	138	43	SECONDARY	1
867	138	57	SECONDARY	1
868	141	41	SECONDARY	1
869	141	40	SECONDARY	1
870	141	57	SECONDARY	1
871	141	50	SECONDARY	1
872	142	52	SECONDARY	1
873	142	40	SECONDARY	1
874	146	45	SECONDARY	1
875	148	42	SECONDARY	1
876	148	41	SECONDARY	1
877	148	40	SECONDARY	1
878	149	51	SECONDARY	1
879	150	45	SECONDARY	1
880	153	57	SECONDARY	1
881	153	50	SECONDARY	1
882	226	49	SECONDARY	1
883	154	56	SECONDARY	1
884	154	42	SECONDARY	1
885	154	41	SECONDARY	1
886	154	40	SECONDARY	1
887	50	45	SECONDARY	1
888	156	40	SECONDARY	1
889	158	42	SECONDARY	1
890	158	41	SECONDARY	1
891	158	40	SECONDARY	1
892	159	49	SECONDARY	1
893	159	57	SECONDARY	1
894	160	40	SECONDARY	1
895	161	49	SECONDARY	1
896	161	44	SECONDARY	1
897	165	42	SECONDARY	1
898	165	41	SECONDARY	1
899	166	41	SECONDARY	1
900	167	56	SECONDARY	1
901	167	42	SECONDARY	1
902	167	41	SECONDARY	1
903	167	40	SECONDARY	1
904	168	41	SECONDARY	1
905	168	40	SECONDARY	1
906	172	57	SECONDARY	1
907	173	57	SECONDARY	1
908	174	57	SECONDARY	1
909	175	43	SECONDARY	1
910	175	41	SECONDARY	1
911	175	40	SECONDARY	1
912	175	54	SECONDARY	1
913	175	39	SECONDARY	1
914	175	45	SECONDARY	1
915	54	39	SECONDARY	1
916	55	55	SECONDARY	1
917	179	52	SECONDARY	1
918	179	57	SECONDARY	1
919	179	50	SECONDARY	1
920	181	52	SECONDARY	1
921	181	49	SECONDARY	1
922	181	42	SECONDARY	1
923	181	51	SECONDARY	1
924	181	41	SECONDARY	1
925	181	40	SECONDARY	1
926	181	57	SECONDARY	1
927	181	39	SECONDARY	1
928	181	45	SECONDARY	1
929	182	40	SECONDARY	1
930	182	57	SECONDARY	1
931	183	41	SECONDARY	1
932	183	40	SECONDARY	1
933	183	57	SECONDARY	1
934	187	56	SECONDARY	1
935	187	54	SECONDARY	1
936	188	40	SECONDARY	1
937	188	39	SECONDARY	1
938	184	52	SECONDARY	1
939	185	39	SECONDARY	1
940	185	50	SECONDARY	1
941	186	41	SECONDARY	1
942	186	40	SECONDARY	1
943	186	57	SECONDARY	1
944	186	50	SECONDARY	1
945	56	52	SECONDARY	1
946	190	52	SECONDARY	1
947	192	41	SECONDARY	1
948	192	54	SECONDARY	1
949	192	57	SECONDARY	1
950	193	52	SECONDARY	1
951	193	42	SECONDARY	1
952	193	43	SECONDARY	1
953	193	40	SECONDARY	1
954	193	39	SECONDARY	1
955	193	50	SECONDARY	1
956	57	53	SECONDARY	1
957	195	51	SECONDARY	1
958	196	42	SECONDARY	1
959	196	39	SECONDARY	1
960	197	42	SECONDARY	1
961	197	41	SECONDARY	1
962	197	39	SECONDARY	1
963	224	40	SECONDARY	1
964	198	52	SECONDARY	1
965	198	43	SECONDARY	1
966	198	41	SECONDARY	1
967	198	40	SECONDARY	1
968	198	54	SECONDARY	1
969	198	57	SECONDARY	1
970	198	39	SECONDARY	1
971	198	45	SECONDARY	1
972	198	50	SECONDARY	1
973	199	49	SECONDARY	1
974	199	51	SECONDARY	1
975	199	57	SECONDARY	1
976	201	57	SECONDARY	1
977	58	46	SECONDARY	1
978	66	42	SECONDARY	1
979	364	42	SECONDARY	1
980	364	41	SECONDARY	1
981	364	39	SECONDARY	1
982	47	51	SECONDARY	1
983	211	49	SECONDARY	1
984	211	44	SECONDARY	1
988	214	42	SECONDARY	1
989	214	39	SECONDARY	1
993	30	45	SECONDARY	1
994	31	39	SECONDARY	1
995	31	41	SECONDARY	1
996	31	40	SECONDARY	1
997	31	45	SECONDARY	1
998	32	39	SECONDARY	1
999	32	41	SECONDARY	1
1000	32	45	SECONDARY	1
1001	32	47	SECONDARY	1
1002	33	39	SECONDARY	1
1003	33	41	SECONDARY	1
1004	33	47	SECONDARY	1
1005	33	50	SECONDARY	1
1006	331	54	SECONDARY	1
1007	230	43	SECONDARY	1
1008	230	51	SECONDARY	1
1009	230	44	SECONDARY	1
1010	230	57	SECONDARY	1
1011	234	41	SECONDARY	1
1018	241	42	SECONDARY	1
1019	241	39	SECONDARY	1
1020	241	50	SECONDARY	1
1021	243	57	SECONDARY	1
1022	243	50	SECONDARY	1
1023	244	57	SECONDARY	1
1024	246	42	SECONDARY	1
1025	246	40	SECONDARY	1
1026	247	51	SECONDARY	1
1027	247	45	SECONDARY	1
1028	248	51	SECONDARY	1
1029	248	41	SECONDARY	1
1030	248	40	SECONDARY	1
1031	248	45	SECONDARY	1
1032	250	43	SECONDARY	1
1033	250	50	SECONDARY	1
1034	251	51	SECONDARY	1
1035	249	42	SECONDARY	1
1036	249	41	SECONDARY	1
1037	249	40	SECONDARY	1
1038	255	49	SECONDARY	1
1039	255	44	SECONDARY	1
1040	255	57	SECONDARY	1
1041	256	42	SECONDARY	1
1042	256	41	SECONDARY	1
1043	258	51	SECONDARY	1
1047	261	49	SECONDARY	1
1048	261	51	SECONDARY	1
1049	261	57	SECONDARY	1
1050	265	54	SECONDARY	1
1051	266	52	SECONDARY	1
1052	266	49	SECONDARY	1
1053	266	42	SECONDARY	1
1054	266	51	SECONDARY	1
1055	266	41	SECONDARY	1
1056	266	40	SECONDARY	1
1057	266	54	SECONDARY	1
1058	266	57	SECONDARY	1
1059	266	45	SECONDARY	1
1060	279	40	SECONDARY	1
1061	273	49	SECONDARY	1
1062	273	44	SECONDARY	1
1063	273	45	SECONDARY	1
1064	274	49	SECONDARY	1
1065	274	51	SECONDARY	1
1066	274	57	SECONDARY	1
1067	276	43	SECONDARY	1
990	30	39	PRIMARY	1
1068	276	50	SECONDARY	1
1069	277	42	SECONDARY	1
1070	277	41	SECONDARY	1
1071	277	40	SECONDARY	1
1072	278	42	SECONDARY	1
1073	278	40	SECONDARY	1
1074	281	42	SECONDARY	1
1075	281	41	SECONDARY	1
1076	281	40	SECONDARY	1
1077	283	42	SECONDARY	1
1078	283	51	SECONDARY	1
1079	283	44	SECONDARY	1
1080	283	57	SECONDARY	1
1081	284	57	SECONDARY	1
1082	285	49	SECONDARY	1
1083	285	45	SECONDARY	1
1084	286	41	SECONDARY	1
1085	286	57	SECONDARY	1
1086	287	43	SECONDARY	1
1087	287	57	SECONDARY	1
1088	287	50	SECONDARY	1
1089	308	42	SECONDARY	1
1090	308	43	SECONDARY	1
1091	308	51	SECONDARY	1
1092	308	41	SECONDARY	1
1093	308	40	SECONDARY	1
1094	308	54	SECONDARY	1
1095	308	57	SECONDARY	1
1096	308	45	SECONDARY	1
1097	308	50	SECONDARY	1
1098	280	56	SECONDARY	1
1099	280	42	SECONDARY	1
1100	280	41	SECONDARY	1
1101	280	40	SECONDARY	1
1102	290	57	SECONDARY	1
1103	291	57	SECONDARY	1
1104	292	49	SECONDARY	1
1105	295	43	SECONDARY	1
1106	295	44	SECONDARY	1
1107	293	41	SECONDARY	1
1108	298	44	SECONDARY	1
1109	298	57	SECONDARY	1
1110	298	50	SECONDARY	1
1111	300	43	SECONDARY	1
1112	300	57	SECONDARY	1
1113	301	43	SECONDARY	1
1114	301	44	SECONDARY	1
1115	301	57	SECONDARY	1
1116	302	43	SECONDARY	1
1117	302	44	SECONDARY	1
1118	302	57	SECONDARY	1
1119	303	43	SECONDARY	1
1120	303	54	SECONDARY	1
1121	303	57	SECONDARY	1
1122	306	41	SECONDARY	1
1123	307	41	SECONDARY	1
1124	307	40	SECONDARY	1
1127	312	41	SECONDARY	1
1128	312	40	SECONDARY	1
1129	312	57	SECONDARY	1
1130	315	57	SECONDARY	1
1131	315	50	SECONDARY	1
1132	316	56	SECONDARY	1
1133	316	41	SECONDARY	1
1134	316	54	SECONDARY	1
1135	320	57	SECONDARY	1
1136	322	52	SECONDARY	1
1137	322	56	SECONDARY	1
1138	322	42	SECONDARY	1
1139	322	41	SECONDARY	1
1140	322	40	SECONDARY	1
1141	322	54	SECONDARY	1
1142	325	56	SECONDARY	1
1143	325	42	SECONDARY	1
1144	325	41	SECONDARY	1
1145	325	40	SECONDARY	1
1146	327	52	SECONDARY	1
1147	327	51	SECONDARY	1
1148	329	56	SECONDARY	1
1149	329	42	SECONDARY	1
1150	329	41	SECONDARY	1
1151	329	39	SECONDARY	1
1152	333	42	SECONDARY	1
1153	333	41	SECONDARY	1
1154	333	40	SECONDARY	1
1155	337	43	SECONDARY	1
1156	337	57	SECONDARY	1
1157	338	52	SECONDARY	1
1158	338	57	SECONDARY	1
1159	338	50	SECONDARY	1
1160	340	56	SECONDARY	1
1161	340	41	SECONDARY	1
1162	340	40	SECONDARY	1
1163	340	39	SECONDARY	1
1164	340	57	SECONDARY	1
1165	343	56	SECONDARY	1
1166	343	42	SECONDARY	1
1167	343	41	SECONDARY	1
1168	343	40	SECONDARY	1
1169	343	39	SECONDARY	1
1170	346	42	SECONDARY	1
1171	346	41	SECONDARY	1
1172	346	39	SECONDARY	1
1173	350	43	SECONDARY	1
1174	350	57	SECONDARY	1
1175	350	50	SECONDARY	1
1176	347	52	SECONDARY	1
1177	347	44	SECONDARY	1
1178	347	54	SECONDARY	1
1186	356	42	SECONDARY	1
1189	367	49	SECONDARY	1
1190	367	44	SECONDARY	1
1191	368	49	SECONDARY	1
1192	368	57	SECONDARY	1
1013	26	57	SECONDARY	1
681	7	41	PRIMARY	1
682	7	54	PRIMARY	0.9
1193	7	40	PRIMARY	0.85
1194	7	39	SECONDARY	0.4
683	7	44	SECONDARY	0.5
1195	1	39	PRIMARY	1
666	1	41	PRIMARY	0.95
667	1	40	PRIMARY	0.7
1196	1	54	SECONDARY	0.8
1197	1	56	SECONDARY	0.3
1198	2	39	PRIMARY	1
669	2	41	PRIMARY	0.85
670	2	52	SECONDARY	0.7
1199	2	54	SECONDARY	0.5
1200	13	43	PRIMARY	1
696	13	50	PRIMARY	0.7
695	13	47	SECONDARY	0.6
1201	26	44	PRIMARY	1
727	26	49	PRIMARY	0.7
728	26	45	SECONDARY	0.5
1202	26	46	SECONDARY	0.4
1203	27	44	PRIMARY	1
730	27	49	PRIMARY	0.9
1204	27	51	SECONDARY	0.6
731	27	45	SECONDARY	0.4
1205	22	44	PRIMARY	1
716	22	45	PRIMARY	0.9
718	22	49	PRIMARY	0.6
717	22	46	SECONDARY	0.5
1206	22	54	SECONDARY	0.7
707	18	48	PRIMARY	1
706	18	50	PRIMARY	0.7
1207	18	43	SECONDARY	0.3
991	30	41	PRIMARY	0.95
992	30	40	PRIMARY	0.8
1208	30	44	SECONDARY	0.5
1209	30	48	SECONDARY	0.6
1211	563	50	PRIMARY	1
1212	563	43	SECONDARY	0.5
1213	563	48	SECONDARY	0.5
1214	564	39	PRIMARY	1
1215	564	42	SECONDARY	0.5
1216	564	41	SECONDARY	0.5
1217	564	40	SECONDARY	0.5
1218	565	52	PRIMARY	1
1223	568	39	PRIMARY	1
1224	568	41	SECONDARY	0.5
1225	568	40	SECONDARY	0.5
1187	623	40	SECONDARY	1
1188	623	39	SECONDARY	1
1125	624	49	SECONDARY	1
1126	624	57	SECONDARY	1
1226	569	52	PRIMARY	1
1231	571	43	PRIMARY	1
1232	571	48	SECONDARY	0.5
1233	571	50	SECONDARY	0.5
1234	572	50	PRIMARY	1
1235	572	52	SECONDARY	0.5
1236	572	43	SECONDARY	0.5
1237	572	48	SECONDARY	0.5
1238	573	52	PRIMARY	1
1242	577	50	PRIMARY	1
1243	577	43	SECONDARY	0.5
1244	577	48	SECONDARY	0.5
1245	578	39	PRIMARY	1
1246	578	58	SECONDARY	0.5
1247	578	56	SECONDARY	0.5
1248	578	42	SECONDARY	0.5
1249	578	41	SECONDARY	0.5
1250	578	40	SECONDARY	0.5
1251	154	58	SECONDARY	0.5
1252	579	52	PRIMARY	1
1253	580	52	PRIMARY	1
1254	581	39	PRIMARY	1
1255	581	42	SECONDARY	0.5
1256	581	41	SECONDARY	0.5
1257	581	40	SECONDARY	0.5
1258	582	52	PRIMARY	1
1259	583	40	PRIMARY	1
1262	585	52	PRIMARY	1
1263	586	58	PRIMARY	1
1264	586	56	SECONDARY	0.5
1265	587	54	PRIMARY	1
1266	587	41	SECONDARY	0.5
1267	587	40	SECONDARY	0.5
1271	589	50	PRIMARY	1
1272	589	43	SECONDARY	0.5
1273	589	48	SECONDARY	0.5
1274	590	43	PRIMARY	1
1275	590	52	SECONDARY	0.5
1276	590	48	SECONDARY	0.5
1277	590	50	SECONDARY	0.5
1282	592	43	PRIMARY	1
1283	592	52	SECONDARY	0.5
1284	592	48	SECONDARY	0.5
1285	592	50	SECONDARY	0.5
1286	593	43	PRIMARY	1
1287	593	48	SECONDARY	0.5
1288	593	50	SECONDARY	0.5
1289	179	48	SECONDARY	0.5
1290	594	52	PRIMARY	1
1291	595	52	PRIMARY	1
1292	341	58	SECONDARY	0.5
1293	596	56	PRIMARY	1
1294	596	58	SECONDARY	0.5
1295	596	42	SECONDARY	0.5
1296	596	41	SECONDARY	0.5
1297	596	40	SECONDARY	0.5
1298	596	39	SECONDARY	0.5
1301	598	52	PRIMARY	1
1304	600	40	PRIMARY	1
1305	600	42	SECONDARY	0.5
1306	600	41	SECONDARY	0.5
1307	600	54	SECONDARY	0.5
1309	602	50	PRIMARY	1
1310	602	44	SECONDARY	0.5
1311	603	43	PRIMARY	1
1312	603	48	SECONDARY	0.5
1313	603	50	SECONDARY	0.5
1317	605	43	PRIMARY	1
1318	605	52	SECONDARY	0.5
1319	605	48	SECONDARY	0.5
1320	605	50	SECONDARY	0.5
1327	608	43	PRIMARY	1
1328	608	52	SECONDARY	0.5
1329	608	48	SECONDARY	0.5
1330	608	50	SECONDARY	0.5
1334	243	48	SECONDARY	0.5
1335	610	39	PRIMARY	1
1336	611	39	PRIMARY	1
1337	611	42	SECONDARY	0.5
1338	611	40	SECONDARY	0.5
1339	612	39	PRIMARY	1
1340	612	41	SECONDARY	0.5
1341	612	40	SECONDARY	0.5
1342	269	48	SECONDARY	0.5
1343	613	52	PRIMARY	1
1344	614	52	PRIMARY	1
1345	615	52	PRIMARY	1
1346	615	48	SECONDARY	0.5
1347	616	43	PRIMARY	1
1348	616	48	SECONDARY	0.5
1349	616	50	SECONDARY	0.5
1351	287	48	SECONDARY	0.5
1352	618	39	PRIMARY	1
1353	618	42	SECONDARY	0.5
1354	618	41	SECONDARY	0.5
1355	618	40	SECONDARY	0.5
1358	620	39	PRIMARY	1
1359	620	42	SECONDARY	0.5
1360	620	41	SECONDARY	0.5
1361	620	40	SECONDARY	0.5
1362	621	50	PRIMARY	1
1363	622	39	PRIMARY	1
1364	622	42	SECONDARY	0.5
1365	622	41	SECONDARY	0.5
1366	622	40	SECONDARY	0.5
1367	622	48	SECONDARY	0.5
1368	623	41	PRIMARY	1
1369	623	40	SECONDARY	0.5
1370	623	39	SECONDARY	0.5
1371	624	44	PRIMARY	1
1372	624	49	SECONDARY	0.5
1373	624	59	SECONDARY	0.5
1374	624	48	SECONDARY	0.5
1375	625	44	PRIMARY	1
1376	625	49	SECONDARY	0.5
1377	625	59	SECONDARY	0.5
1378	625	48	SECONDARY	0.5
1379	30	40	PRIMARY	1
1380	30	42	SECONDARY	0.5
1381	30	51	SECONDARY	0.5
1382	30	41	SECONDARY	0.5
1227	27	44	PRIMARY	1
1228	27	49	SECONDARY	0.5
1229	27	51	SECONDARY	0.5
1230	27	59	SECONDARY	0.5
1314	26	44	PRIMARY	1
1315	26	49	SECONDARY	0.5
1316	26	59	SECONDARY	0.5
1331	16	43	PRIMARY	1
1332	16	48	SECONDARY	0.5
1333	16	50	SECONDARY	0.5
1387	627	40	PRIMARY	1
1388	627	51	SECONDARY	0.5
1389	627	41	SECONDARY	0.5
1390	627	54	SECONDARY	0.5
1391	627	39	SECONDARY	0.5
1392	627	45	SECONDARY	0.5
1393	628	39	PRIMARY	1
1394	628	51	SECONDARY	0.5
1395	628	41	SECONDARY	0.5
1396	628	40	SECONDARY	0.5
1397	628	54	SECONDARY	0.5
1398	628	45	SECONDARY	0.5
1399	629	45	PRIMARY	1
1400	629	51	SECONDARY	0.5
1401	629	48	SECONDARY	0.5
1410	631	39	PRIMARY	1
1411	631	42	SECONDARY	0.5
1412	631	41	SECONDARY	0.5
1413	631	40	SECONDARY	0.5
1414	631	48	SECONDARY	0.5
1415	631	45	SECONDARY	0.5
1416	632	39	PRIMARY	1
1417	632	52	SECONDARY	0.5
1418	632	42	SECONDARY	0.5
1419	632	41	SECONDARY	0.5
1420	632	40	SECONDARY	0.5
1421	633	39	PRIMARY	1
1422	633	42	SECONDARY	0.5
1423	633	51	SECONDARY	0.5
1424	633	41	SECONDARY	0.5
1425	633	40	SECONDARY	0.5
1426	633	54	SECONDARY	0.5
1427	633	48	SECONDARY	0.5
1428	633	45	SECONDARY	0.5
1429	634	39	PRIMARY	1
1430	634	42	SECONDARY	0.5
1431	634	51	SECONDARY	0.5
1432	634	41	SECONDARY	0.5
1433	634	40	SECONDARY	0.5
1434	634	54	SECONDARY	0.5
1435	634	48	SECONDARY	0.5
1436	634	45	SECONDARY	0.5
1437	635	40	PRIMARY	1
1438	635	52	SECONDARY	0.5
1439	635	42	SECONDARY	0.5
1440	635	51	SECONDARY	0.5
1441	635	41	SECONDARY	0.5
1442	635	54	SECONDARY	0.5
1443	635	39	SECONDARY	0.5
1444	635	48	SECONDARY	0.5
1445	635	45	SECONDARY	0.5
1455	637	39	PRIMARY	1
1456	637	52	SECONDARY	0.5
1457	637	51	SECONDARY	0.5
1458	637	41	SECONDARY	0.5
1459	637	40	SECONDARY	0.5
1460	637	48	SECONDARY	0.5
1461	637	50	SECONDARY	0.5
1462	638	48	PRIMARY	1
1463	638	41	SECONDARY	0.5
1464	638	40	SECONDARY	0.5
1465	638	39	SECONDARY	0.5
1466	638	50	SECONDARY	0.5
1467	639	39	PRIMARY	1
1468	639	52	SECONDARY	0.5
1469	639	42	SECONDARY	0.5
1470	640	41	PRIMARY	1
1471	640	42	SECONDARY	0.5
1472	640	40	SECONDARY	0.5
1473	640	39	SECONDARY	0.5
1474	641	40	PRIMARY	1
1475	641	41	SECONDARY	0.5
1476	641	54	SECONDARY	0.5
1477	641	39	SECONDARY	0.5
1478	641	48	SECONDARY	0.5
1479	641	50	SECONDARY	0.5
1480	642	39	PRIMARY	1
1481	642	42	SECONDARY	0.5
1482	642	41	SECONDARY	0.5
1483	642	40	SECONDARY	0.5
1484	643	39	PRIMARY	1
1485	643	52	SECONDARY	0.5
1486	643	42	SECONDARY	0.5
1487	643	41	SECONDARY	0.5
1488	643	40	SECONDARY	0.5
1489	643	54	SECONDARY	0.5
1490	643	48	SECONDARY	0.5
1491	643	50	SECONDARY	0.5
1492	644	40	PRIMARY	1
1493	644	39	SECONDARY	0.5
1494	645	39	PRIMARY	1
1495	645	52	SECONDARY	0.5
1496	645	42	SECONDARY	0.5
1497	645	41	SECONDARY	0.5
1498	645	40	SECONDARY	0.5
1499	645	48	SECONDARY	0.5
1500	645	50	SECONDARY	0.5
1501	646	40	PRIMARY	1
1502	646	42	SECONDARY	0.5
1503	646	41	SECONDARY	0.5
1504	646	54	SECONDARY	0.5
1505	646	39	SECONDARY	0.5
1506	646	48	SECONDARY	0.5
1507	646	45	SECONDARY	0.5
1508	646	50	SECONDARY	0.5
1509	647	39	PRIMARY	1
1510	647	42	SECONDARY	0.5
1511	647	51	SECONDARY	0.5
1512	647	41	SECONDARY	0.5
1513	647	40	SECONDARY	0.5
1514	647	54	SECONDARY	0.5
1515	647	48	SECONDARY	0.5
1516	647	45	SECONDARY	0.5
1517	647	50	SECONDARY	0.5
1518	648	48	PRIMARY	1
1519	648	39	SECONDARY	0.5
1520	648	50	SECONDARY	0.5
1521	649	48	PRIMARY	1
1522	649	42	SECONDARY	0.5
1523	649	39	SECONDARY	0.5
1524	649	50	SECONDARY	0.5
1533	32	39	PRIMARY	1
1534	32	49	SECONDARY	0.5
1535	32	41	SECONDARY	0.5
1402	33	48	PRIMARY	1
1403	33	52	SECONDARY	0.5
1404	33	41	SECONDARY	0.5
1405	33	40	SECONDARY	0.5
1406	33	54	SECONDARY	0.5
1407	33	39	SECONDARY	0.5
1408	33	45	SECONDARY	0.5
1525	247	48	PRIMARY	1
1526	247	51	SECONDARY	0.5
1527	247	45	SECONDARY	0.5
1547	654	40	PRIMARY	1
1548	654	51	SECONDARY	0.5
1549	654	41	SECONDARY	0.5
1550	654	40	SECONDARY	0.5
1551	654	54	SECONDARY	0.5
1552	654	39	SECONDARY	0.5
1553	654	45	SECONDARY	0.5
1554	655	45	PRIMARY	1
1555	655	51	SECONDARY	0.5
1556	655	48	SECONDARY	0.5
1557	656	39	PRIMARY	1
1558	656	42	SECONDARY	0.5
1559	656	51	SECONDARY	0.5
1560	656	41	SECONDARY	0.5
1561	656	40	SECONDARY	0.5
1562	656	54	SECONDARY	0.5
1563	656	48	SECONDARY	0.5
1564	656	45	SECONDARY	0.5
1565	656	50	SECONDARY	0.5
1566	657	39	PRIMARY	1
1567	657	42	SECONDARY	0.5
1568	657	51	SECONDARY	0.5
1569	657	41	SECONDARY	0.5
1570	657	40	SECONDARY	0.5
1571	657	54	SECONDARY	0.5
1572	657	48	SECONDARY	0.5
1573	657	45	SECONDARY	0.5
1574	658	39	PRIMARY	1
1575	658	41	SECONDARY	0.5
1576	658	40	SECONDARY	0.5
1577	658	48	SECONDARY	0.5
1578	658	50	SECONDARY	0.5
1579	659	40	PRIMARY	1
1580	659	42	SECONDARY	0.5
1581	659	51	SECONDARY	0.5
1582	659	41	SECONDARY	0.5
1583	659	40	SECONDARY	0.5
1584	659	54	SECONDARY	0.5
1585	659	39	SECONDARY	0.5
1586	659	48	SECONDARY	0.5
1587	659	45	SECONDARY	0.5
1588	659	50	SECONDARY	0.5
1594	662	43	PRIMARY	1
1595	662	48	SECONDARY	0.5
1599	666	54	PRIMARY	1
1600	666	59	SECONDARY	0.5
1601	666	45	SECONDARY	0.5
1602	120	48	SECONDARY	0.5
1603	123	59	SECONDARY	0.5
1604	667	54	PRIMARY	1
1605	667	52	SECONDARY	0.5
1606	667	58	SECONDARY	0.5
1607	667	41	SECONDARY	0.5
1608	667	40	SECONDARY	0.5
1609	667	39	SECONDARY	0.5
1610	668	54	PRIMARY	1
1611	668	58	SECONDARY	0.5
1612	668	41	SECONDARY	0.5
1613	669	43	PRIMARY	1
1614	669	59	SECONDARY	0.5
1615	335	48	SECONDARY	0.5
1616	670	42	PRIMARY	1
1617	671	56	PRIMARY	1
1618	672	40	PRIMARY	1
1619	673	58	PRIMARY	1
1620	674	58	PRIMARY	1
1622	187	58	SECONDARY	0.5
1623	676	39	PRIMARY	1
1624	676	39	SECONDARY	0.5
1626	678	40	PRIMARY	1
1627	679	54	PRIMARY	1
1628	680	40	PRIMARY	1
1629	680	42	SECONDARY	0.5
1631	682	44	PRIMARY	1
1632	683	44	PRIMARY	1
1633	683	50	SECONDARY	0.5
1634	542	43	SECONDARY	0.5
1635	542	51	SECONDARY	0.5
1636	542	44	SECONDARY	0.5
1637	542	50	SECONDARY	0.5
1638	684	42	PRIMARY	1
1639	685	42	PRIMARY	1
1641	687	42	PRIMARY	1
1642	244	48	SECONDARY	0.5
1644	689	48	PRIMARY	1
1645	689	49	SECONDARY	0.5
1646	689	43	SECONDARY	0.5
1647	690	42	PRIMARY	1
1648	690	40	SECONDARY	0.5
1649	690	54	SECONDARY	0.5
1650	691	40	PRIMARY	1
1651	691	42	SECONDARY	0.5
1652	692	40	PRIMARY	1
1653	692	42	SECONDARY	0.5
1654	693	52	PRIMARY	1
1655	694	48	PRIMARY	1
1656	694	45	SECONDARY	0.5
1657	695	48	PRIMARY	1
1658	695	44	SECONDARY	0.5
1659	696	48	PRIMARY	1
1660	697	44	PRIMARY	1
1661	698	56	PRIMARY	1
1662	698	40	SECONDARY	0.5
1663	699	48	PRIMARY	1
1664	699	51	SECONDARY	0.5
1665	699	44	SECONDARY	0.5
1666	700	39	PRIMARY	1
1667	700	58	SECONDARY	0.5
1668	700	41	SECONDARY	0.5
1669	700	40	SECONDARY	0.5
1670	701	49	PRIMARY	1
1671	701	43	SECONDARY	0.5
1672	701	48	SECONDARY	0.5
1675	703	40	PRIMARY	1
1676	704	39	PRIMARY	1
1677	705	52	PRIMARY	1
1678	706	42	PRIMARY	1
1679	707	52	PRIMARY	1
1680	708	50	PRIMARY	1
1681	708	48	SECONDARY	0.5
1687	711	48	PRIMARY	1
1688	711	43	SECONDARY	0.5
1689	711	44	SECONDARY	0.5
1383	30	54	SECONDARY	0.5
1384	30	39	SECONDARY	0.5
1385	30	48	SECONDARY	0.5
1386	30	45	SECONDARY	0.5
1536	32	40	SECONDARY	0.5
1537	32	54	SECONDARY	0.5
1538	32	48	SECONDARY	0.5
1539	32	45	SECONDARY	0.5
1540	32	50	SECONDARY	0.5
1409	33	50	SECONDARY	0.5
1589	316	40	PRIMARY	1
1590	316	56	SECONDARY	0.5
1541	546	39	PRIMARY	1
1542	546	42	SECONDARY	0.5
1543	546	41	SECONDARY	0.5
1544	546	40	SECONDARY	0.5
1591	316	41	SECONDARY	0.5
1592	316	54	SECONDARY	0.5
1545	546	48	SECONDARY	0.5
1546	546	50	SECONDARY	0.5
619	186	41	SECONDARY	1
620	186	40	SECONDARY	1
621	186	54	SECONDARY	1
672	491	41	SECONDARY	1
673	491	52	SECONDARY	1
1241	131	52	PRIMARY	1
1350	131	52	PRIMARY	1
597	389	42	SECONDARY	1
598	389	41	SECONDARY	1
599	389	39	SECONDARY	1
1643	245	39	PRIMARY	1
1640	231	41	PRIMARY	1
1684	369	40	PRIMARY	1
1685	369	54	SECONDARY	0.5
1686	369	59	SECONDARY	0.5
1593	75	42	PRIMARY	1
1598	116	42	PRIMARY	1
1596	98	49	PRIMARY	1
1625	194	44	PRIMARY	1
1014	16	43	SECONDARY	1
1015	16	57	SECONDARY	1
1016	16	57	SECONDARY	1
1017	16	50	SECONDARY	1
1268	16	43	PRIMARY	1
1269	16	48	SECONDARY	0.5
1270	16	50	SECONDARY	0.5
1278	16	43	PRIMARY	1
1279	16	52	SECONDARY	0.5
1280	16	48	SECONDARY	0.5
1281	16	50	SECONDARY	0.5
1321	16	50	PRIMARY	1
1322	16	43	SECONDARY	0.5
1323	16	48	SECONDARY	0.5
1324	16	43	PRIMARY	1
1325	16	48	SECONDARY	0.5
1326	16	50	SECONDARY	0.5
1446	635	40	PRIMARY	1
1447	635	52	SECONDARY	0.5
1448	635	42	SECONDARY	0.5
1449	635	51	SECONDARY	0.5
1450	635	41	SECONDARY	0.5
1451	635	54	SECONDARY	0.5
1452	635	39	SECONDARY	0.5
1453	635	48	SECONDARY	0.5
1454	635	45	SECONDARY	0.5
985	512	43	SECONDARY	1
986	512	40	SECONDARY	1
987	512	57	SECONDARY	1
644	383	42	SECONDARY	1
645	383	40	SECONDARY	1
1528	8	40	PRIMARY	1
1529	8	51	SECONDARY	0.5
1530	8	41	SECONDARY	0.5
1531	8	54	SECONDARY	0.5
1532	8	45	SECONDARY	0.5
613	692	42	SECONDARY	1
713	501	50	SECONDARY	1
714	501	52	SECONDARY	1
715	501	45	SECONDARY	1
1260	501	48	PRIMARY	1
1261	501	50	SECONDARY	0.5
1044	502	43	SECONDARY	1
1045	502	57	SECONDARY	1
1046	502	52	SECONDARY	1
1682	708	50	PRIMARY	1
1683	708	44	SECONDARY	0.5
1	712	39	PRIMARY	1
2	712	52	SECONDARY	0.5
3	712	43	SECONDARY	0.5
4	712	50	SECONDARY	0.5
5	713	57	PRIMARY	1
6	714	52	PRIMARY	1
7	714	55	SECONDARY	0.5
8	715	52	PRIMARY	1
9	715	55	SECONDARY	0.5
10	716	39	PRIMARY	1
11	716	41	SECONDARY	0.5
12	716	40	SECONDARY	0.5
13	716	52	SECONDARY	0.5
14	717	39	PRIMARY	1
15	717	41	SECONDARY	0.5
16	717	40	SECONDARY	0.5
17	717	52	SECONDARY	0.5
18	712	39	PRIMARY	1
19	712	52	SECONDARY	0.5
20	712	43	SECONDARY	0.5
21	712	50	SECONDARY	0.5
22	713	57	PRIMARY	1
23	714	52	PRIMARY	1
24	714	55	SECONDARY	0.5
25	715	52	PRIMARY	1
26	715	55	SECONDARY	0.5
27	716	39	PRIMARY	1
28	716	41	SECONDARY	0.5
29	716	40	SECONDARY	0.5
30	716	52	SECONDARY	0.5
31	717	39	PRIMARY	1
32	717	41	SECONDARY	0.5
33	717	40	SECONDARY	0.5
34	717	52	SECONDARY	0.5
\.


--
-- Data for Name: movement_muscle_map_backup_20260301; Type: TABLE DATA; Schema: public; Owner: jacked
--

COPY public.movement_muscle_map_backup_20260301 (id, movement_id, muscle_id, role, magnitude) FROM stdin;
600	76	45	SECONDARY	1
601	123	41	SECONDARY	1
602	123	57	SECONDARY	1
603	227	40	SECONDARY	1
604	227	54	SECONDARY	1
605	259	45	SECONDARY	1
606	269	43	SECONDARY	1
607	269	57	SECONDARY	1
608	40	53	SECONDARY	1
609	41	55	SECONDARY	1
610	42	44	SECONDARY	1
611	42	47	SECONDARY	1
612	270	56	SECONDARY	1
614	294	42	SECONDARY	1
615	299	41	SECONDARY	1
616	299	40	SECONDARY	1
617	305	56	SECONDARY	1
618	305	42	SECONDARY	1
622	324	39	SECONDARY	1
623	330	56	SECONDARY	1
624	332	49	SECONDARY	1
625	332	43	SECONDARY	1
626	335	57	SECONDARY	1
627	358	43	SECONDARY	1
628	369	54	SECONDARY	1
629	369	57	SECONDARY	1
630	370	57	SECONDARY	1
631	371	42	SECONDARY	1
632	371	41	SECONDARY	1
633	371	39	SECONDARY	1
634	43	41	SECONDARY	1
635	43	42	SECONDARY	1
636	44	39	SECONDARY	1
637	44	40	SECONDARY	1
638	45	41	SECONDARY	1
639	45	42	SECONDARY	1
640	46	44	SECONDARY	1
641	46	47	SECONDARY	1
642	235	57	SECONDARY	1
643	235	50	SECONDARY	1
646	341	56	SECONDARY	1
647	341	42	SECONDARY	1
648	341	41	SECONDARY	1
649	341	39	SECONDARY	1
650	152	42	SECONDARY	1
651	152	41	SECONDARY	1
652	152	40	SECONDARY	1
653	180	41	SECONDARY	1
654	180	40	SECONDARY	1
655	289	42	SECONDARY	1
656	289	41	SECONDARY	1
657	289	40	SECONDARY	1
658	296	42	SECONDARY	1
659	296	41	SECONDARY	1
660	296	40	SECONDARY	1
661	101	40	SECONDARY	1
662	104	51	SECONDARY	1
663	104	41	SECONDARY	1
664	104	40	SECONDARY	1
665	104	54	SECONDARY	1
668	1	52	SECONDARY	1
671	2	45	SECONDARY	1
674	4	41	SECONDARY	1
675	4	55	SECONDARY	1
676	4	52	SECONDARY	1
677	5	41	SECONDARY	1
678	5	40	SECONDARY	1
679	6	41	SECONDARY	1
680	6	40	SECONDARY	1
684	7	51	SECONDARY	1
685	8	41	SECONDARY	1
686	8	54	SECONDARY	1
687	9	41	SECONDARY	1
688	9	52	SECONDARY	1
689	10	40	SECONDARY	1
690	11	41	SECONDARY	1
691	11	54	SECONDARY	1
692	12	40	SECONDARY	1
693	12	52	SECONDARY	1
694	12	44	SECONDARY	1
697	14	47	SECONDARY	1
698	14	50	SECONDARY	1
699	15	47	SECONDARY	1
700	15	50	SECONDARY	1
701	16	47	SECONDARY	1
702	16	50	SECONDARY	1
703	16	52	SECONDARY	1
704	17	50	SECONDARY	1
705	17	47	SECONDARY	1
708	18	52	SECONDARY	1
709	19	50	SECONDARY	1
710	19	48	SECONDARY	1
711	20	50	SECONDARY	1
712	20	52	SECONDARY	1
719	23	45	SECONDARY	1
720	23	46	SECONDARY	1
721	23	49	SECONDARY	1
722	24	45	SECONDARY	1
723	24	49	SECONDARY	1
724	25	44	SECONDARY	1
725	25	46	SECONDARY	1
726	25	49	SECONDARY	1
729	26	52	SECONDARY	1
732	28	49	SECONDARY	1
733	28	45	SECONDARY	1
734	29	43	SECONDARY	1
735	29	50	SECONDARY	1
736	29	52	SECONDARY	1
737	37	53	SECONDARY	1
738	37	47	SECONDARY	1
739	38	52	SECONDARY	1
740	38	48	SECONDARY	1
741	39	55	SECONDARY	1
742	59	55	SECONDARY	1
743	59	50	SECONDARY	1
744	60	52	SECONDARY	1
745	60	47	SECONDARY	1
746	61	41	SECONDARY	1
747	64	47	SECONDARY	1
748	64	49	SECONDARY	1
749	127	52	SECONDARY	1
750	127	49	SECONDARY	1
751	127	42	SECONDARY	1
752	127	51	SECONDARY	1
753	127	54	SECONDARY	1
754	127	57	SECONDARY	1
755	127	45	SECONDARY	1
756	65	52	SECONDARY	1
757	65	47	SECONDARY	1
758	65	41	SECONDARY	1
759	62	39	SECONDARY	1
760	62	41	SECONDARY	1
761	62	42	SECONDARY	1
762	34	52	SECONDARY	1
763	34	45	SECONDARY	1
764	34	39	SECONDARY	1
765	35	52	SECONDARY	1
766	35	51	SECONDARY	1
767	35	45	SECONDARY	1
768	36	52	SECONDARY	1
769	36	45	SECONDARY	1
770	63	41	SECONDARY	1
771	63	42	SECONDARY	1
772	63	52	SECONDARY	1
773	70	41	SECONDARY	1
774	70	40	SECONDARY	1
775	70	57	SECONDARY	1
776	222	42	SECONDARY	1
777	222	41	SECONDARY	1
778	222	54	SECONDARY	1
779	222	57	SECONDARY	1
780	77	57	SECONDARY	1
781	78	49	SECONDARY	1
782	78	51	SECONDARY	1
783	78	41	SECONDARY	1
784	78	40	SECONDARY	1
785	78	39	SECONDARY	1
786	79	52	SECONDARY	1
787	79	56	SECONDARY	1
788	79	49	SECONDARY	1
789	79	42	SECONDARY	1
790	79	51	SECONDARY	1
791	79	41	SECONDARY	1
792	79	40	SECONDARY	1
793	79	57	SECONDARY	1
794	79	39	SECONDARY	1
795	79	45	SECONDARY	1
796	80	57	SECONDARY	1
797	80	50	SECONDARY	1
798	81	42	SECONDARY	1
799	81	51	SECONDARY	1
800	81	41	SECONDARY	1
801	81	40	SECONDARY	1
802	81	54	SECONDARY	1
805	83	51	SECONDARY	1
806	84	51	SECONDARY	1
807	85	42	SECONDARY	1
808	85	40	SECONDARY	1
809	87	42	SECONDARY	1
810	87	41	SECONDARY	1
811	87	40	SECONDARY	1
812	87	39	SECONDARY	1
813	88	43	SECONDARY	1
814	88	51	SECONDARY	1
815	89	42	SECONDARY	1
816	89	41	SECONDARY	1
817	89	40	SECONDARY	1
818	90	43	SECONDARY	1
819	90	44	SECONDARY	1
820	90	57	SECONDARY	1
821	90	50	SECONDARY	1
822	97	49	SECONDARY	1
823	97	57	SECONDARY	1
824	95	52	SECONDARY	1
825	95	57	SECONDARY	1
826	95	50	SECONDARY	1
827	99	50	SECONDARY	1
828	93	42	SECONDARY	1
829	93	41	SECONDARY	1
830	93	40	SECONDARY	1
831	94	42	SECONDARY	1
832	94	41	SECONDARY	1
833	94	40	SECONDARY	1
834	225	52	SECONDARY	1
835	225	49	SECONDARY	1
836	225	43	SECONDARY	1
837	102	57	SECONDARY	1
838	110	49	SECONDARY	1
839	110	57	SECONDARY	1
840	117	51	SECONDARY	1
841	389	42	SECONDARY	1
842	389	41	SECONDARY	1
843	389	39	SECONDARY	1
844	118	52	SECONDARY	1
845	118	56	SECONDARY	1
846	118	42	SECONDARY	1
847	118	41	SECONDARY	1
848	118	40	SECONDARY	1
849	118	39	SECONDARY	1
850	119	52	SECONDARY	1
851	119	43	SECONDARY	1
852	119	57	SECONDARY	1
853	121	52	SECONDARY	1
854	121	57	SECONDARY	1
855	121	50	SECONDARY	1
856	124	51	SECONDARY	1
857	124	41	SECONDARY	1
858	124	40	SECONDARY	1
859	124	54	SECONDARY	1
860	124	45	SECONDARY	1
861	124	50	SECONDARY	1
862	125	43	SECONDARY	1
863	125	57	SECONDARY	1
864	120	57	SECONDARY	1
865	130	51	SECONDARY	1
866	138	43	SECONDARY	1
867	138	57	SECONDARY	1
868	141	41	SECONDARY	1
869	141	40	SECONDARY	1
870	141	57	SECONDARY	1
871	141	50	SECONDARY	1
872	142	52	SECONDARY	1
873	142	40	SECONDARY	1
874	146	45	SECONDARY	1
875	148	42	SECONDARY	1
876	148	41	SECONDARY	1
877	148	40	SECONDARY	1
878	149	51	SECONDARY	1
879	150	45	SECONDARY	1
880	153	57	SECONDARY	1
881	153	50	SECONDARY	1
882	226	49	SECONDARY	1
883	154	56	SECONDARY	1
884	154	42	SECONDARY	1
885	154	41	SECONDARY	1
886	154	40	SECONDARY	1
887	50	45	SECONDARY	1
888	156	40	SECONDARY	1
889	158	42	SECONDARY	1
890	158	41	SECONDARY	1
891	158	40	SECONDARY	1
892	159	49	SECONDARY	1
893	159	57	SECONDARY	1
894	160	40	SECONDARY	1
895	161	49	SECONDARY	1
896	161	44	SECONDARY	1
897	165	42	SECONDARY	1
898	165	41	SECONDARY	1
899	166	41	SECONDARY	1
900	167	56	SECONDARY	1
901	167	42	SECONDARY	1
902	167	41	SECONDARY	1
903	167	40	SECONDARY	1
904	168	41	SECONDARY	1
905	168	40	SECONDARY	1
906	172	57	SECONDARY	1
907	173	57	SECONDARY	1
908	174	57	SECONDARY	1
909	175	43	SECONDARY	1
910	175	41	SECONDARY	1
911	175	40	SECONDARY	1
912	175	54	SECONDARY	1
913	175	39	SECONDARY	1
914	175	45	SECONDARY	1
915	54	39	SECONDARY	1
916	55	55	SECONDARY	1
917	179	52	SECONDARY	1
918	179	57	SECONDARY	1
919	179	50	SECONDARY	1
920	181	52	SECONDARY	1
921	181	49	SECONDARY	1
922	181	42	SECONDARY	1
923	181	51	SECONDARY	1
924	181	41	SECONDARY	1
925	181	40	SECONDARY	1
926	181	57	SECONDARY	1
927	181	39	SECONDARY	1
928	181	45	SECONDARY	1
929	182	40	SECONDARY	1
930	182	57	SECONDARY	1
931	183	41	SECONDARY	1
932	183	40	SECONDARY	1
933	183	57	SECONDARY	1
934	187	56	SECONDARY	1
935	187	54	SECONDARY	1
936	188	40	SECONDARY	1
937	188	39	SECONDARY	1
938	184	52	SECONDARY	1
939	185	39	SECONDARY	1
940	185	50	SECONDARY	1
941	186	41	SECONDARY	1
942	186	40	SECONDARY	1
943	186	57	SECONDARY	1
944	186	50	SECONDARY	1
945	56	52	SECONDARY	1
946	190	52	SECONDARY	1
947	192	41	SECONDARY	1
948	192	54	SECONDARY	1
949	192	57	SECONDARY	1
950	193	52	SECONDARY	1
951	193	42	SECONDARY	1
952	193	43	SECONDARY	1
953	193	40	SECONDARY	1
954	193	39	SECONDARY	1
955	193	50	SECONDARY	1
956	57	53	SECONDARY	1
957	195	51	SECONDARY	1
958	196	42	SECONDARY	1
959	196	39	SECONDARY	1
960	197	42	SECONDARY	1
961	197	41	SECONDARY	1
962	197	39	SECONDARY	1
963	224	40	SECONDARY	1
964	198	52	SECONDARY	1
965	198	43	SECONDARY	1
966	198	41	SECONDARY	1
967	198	40	SECONDARY	1
968	198	54	SECONDARY	1
969	198	57	SECONDARY	1
970	198	39	SECONDARY	1
971	198	45	SECONDARY	1
972	198	50	SECONDARY	1
973	199	49	SECONDARY	1
974	199	51	SECONDARY	1
975	199	57	SECONDARY	1
976	201	57	SECONDARY	1
977	58	46	SECONDARY	1
978	66	42	SECONDARY	1
979	364	42	SECONDARY	1
980	364	41	SECONDARY	1
981	364	39	SECONDARY	1
982	47	51	SECONDARY	1
983	211	49	SECONDARY	1
984	211	44	SECONDARY	1
988	214	42	SECONDARY	1
989	214	39	SECONDARY	1
993	30	45	SECONDARY	1
994	31	39	SECONDARY	1
995	31	41	SECONDARY	1
996	31	40	SECONDARY	1
997	31	45	SECONDARY	1
998	32	39	SECONDARY	1
999	32	41	SECONDARY	1
1000	32	45	SECONDARY	1
1001	32	47	SECONDARY	1
1002	33	39	SECONDARY	1
1003	33	41	SECONDARY	1
1004	33	47	SECONDARY	1
1005	33	50	SECONDARY	1
1006	331	54	SECONDARY	1
1007	230	43	SECONDARY	1
1008	230	51	SECONDARY	1
1009	230	44	SECONDARY	1
1010	230	57	SECONDARY	1
1011	234	41	SECONDARY	1
1018	241	42	SECONDARY	1
1019	241	39	SECONDARY	1
1020	241	50	SECONDARY	1
1021	243	57	SECONDARY	1
1022	243	50	SECONDARY	1
1023	244	57	SECONDARY	1
1024	246	42	SECONDARY	1
1025	246	40	SECONDARY	1
1026	247	51	SECONDARY	1
1027	247	45	SECONDARY	1
1028	248	51	SECONDARY	1
1029	248	41	SECONDARY	1
1030	248	40	SECONDARY	1
1031	248	45	SECONDARY	1
1032	250	43	SECONDARY	1
1033	250	50	SECONDARY	1
1034	251	51	SECONDARY	1
1035	249	42	SECONDARY	1
1036	249	41	SECONDARY	1
1037	249	40	SECONDARY	1
1038	255	49	SECONDARY	1
1039	255	44	SECONDARY	1
1040	255	57	SECONDARY	1
1041	256	42	SECONDARY	1
1042	256	41	SECONDARY	1
1043	258	51	SECONDARY	1
1047	261	49	SECONDARY	1
1048	261	51	SECONDARY	1
1049	261	57	SECONDARY	1
1050	265	54	SECONDARY	1
1051	266	52	SECONDARY	1
1052	266	49	SECONDARY	1
1053	266	42	SECONDARY	1
1054	266	51	SECONDARY	1
1055	266	41	SECONDARY	1
1056	266	40	SECONDARY	1
1057	266	54	SECONDARY	1
1058	266	57	SECONDARY	1
1059	266	45	SECONDARY	1
1060	279	40	SECONDARY	1
1061	273	49	SECONDARY	1
1062	273	44	SECONDARY	1
1063	273	45	SECONDARY	1
1064	274	49	SECONDARY	1
1065	274	51	SECONDARY	1
1066	274	57	SECONDARY	1
1067	276	43	SECONDARY	1
990	30	39	PRIMARY	1
1068	276	50	SECONDARY	1
1069	277	42	SECONDARY	1
1070	277	41	SECONDARY	1
1071	277	40	SECONDARY	1
1072	278	42	SECONDARY	1
1073	278	40	SECONDARY	1
1074	281	42	SECONDARY	1
1075	281	41	SECONDARY	1
1076	281	40	SECONDARY	1
1077	283	42	SECONDARY	1
1078	283	51	SECONDARY	1
1079	283	44	SECONDARY	1
1080	283	57	SECONDARY	1
1081	284	57	SECONDARY	1
1082	285	49	SECONDARY	1
1083	285	45	SECONDARY	1
1084	286	41	SECONDARY	1
1085	286	57	SECONDARY	1
1086	287	43	SECONDARY	1
1087	287	57	SECONDARY	1
1088	287	50	SECONDARY	1
1089	308	42	SECONDARY	1
1090	308	43	SECONDARY	1
1091	308	51	SECONDARY	1
1092	308	41	SECONDARY	1
1093	308	40	SECONDARY	1
1094	308	54	SECONDARY	1
1095	308	57	SECONDARY	1
1096	308	45	SECONDARY	1
1097	308	50	SECONDARY	1
1098	280	56	SECONDARY	1
1099	280	42	SECONDARY	1
1100	280	41	SECONDARY	1
1101	280	40	SECONDARY	1
1102	290	57	SECONDARY	1
1103	291	57	SECONDARY	1
1104	292	49	SECONDARY	1
1105	295	43	SECONDARY	1
1106	295	44	SECONDARY	1
1107	293	41	SECONDARY	1
1108	298	44	SECONDARY	1
1109	298	57	SECONDARY	1
1110	298	50	SECONDARY	1
1111	300	43	SECONDARY	1
1112	300	57	SECONDARY	1
1113	301	43	SECONDARY	1
1114	301	44	SECONDARY	1
1115	301	57	SECONDARY	1
1116	302	43	SECONDARY	1
1117	302	44	SECONDARY	1
1118	302	57	SECONDARY	1
1119	303	43	SECONDARY	1
1120	303	54	SECONDARY	1
1121	303	57	SECONDARY	1
1122	306	41	SECONDARY	1
1123	307	41	SECONDARY	1
1124	307	40	SECONDARY	1
1127	312	41	SECONDARY	1
1128	312	40	SECONDARY	1
1129	312	57	SECONDARY	1
1130	315	57	SECONDARY	1
1131	315	50	SECONDARY	1
1132	316	56	SECONDARY	1
1133	316	41	SECONDARY	1
1134	316	54	SECONDARY	1
1135	320	57	SECONDARY	1
1136	322	52	SECONDARY	1
1137	322	56	SECONDARY	1
1138	322	42	SECONDARY	1
1139	322	41	SECONDARY	1
1140	322	40	SECONDARY	1
1141	322	54	SECONDARY	1
1142	325	56	SECONDARY	1
1143	325	42	SECONDARY	1
1144	325	41	SECONDARY	1
1145	325	40	SECONDARY	1
1146	327	52	SECONDARY	1
1147	327	51	SECONDARY	1
1148	329	56	SECONDARY	1
1149	329	42	SECONDARY	1
1150	329	41	SECONDARY	1
1151	329	39	SECONDARY	1
1152	333	42	SECONDARY	1
1153	333	41	SECONDARY	1
1154	333	40	SECONDARY	1
1155	337	43	SECONDARY	1
1156	337	57	SECONDARY	1
1157	338	52	SECONDARY	1
1158	338	57	SECONDARY	1
1159	338	50	SECONDARY	1
1160	340	56	SECONDARY	1
1161	340	41	SECONDARY	1
1162	340	40	SECONDARY	1
1163	340	39	SECONDARY	1
1164	340	57	SECONDARY	1
1165	343	56	SECONDARY	1
1166	343	42	SECONDARY	1
1167	343	41	SECONDARY	1
1168	343	40	SECONDARY	1
1169	343	39	SECONDARY	1
1170	346	42	SECONDARY	1
1171	346	41	SECONDARY	1
1172	346	39	SECONDARY	1
1173	350	43	SECONDARY	1
1174	350	57	SECONDARY	1
1175	350	50	SECONDARY	1
1176	347	52	SECONDARY	1
1177	347	44	SECONDARY	1
1178	347	54	SECONDARY	1
1186	356	42	SECONDARY	1
1189	367	49	SECONDARY	1
1190	367	44	SECONDARY	1
1191	368	49	SECONDARY	1
1192	368	57	SECONDARY	1
1013	26	57	SECONDARY	1
681	7	41	PRIMARY	1
682	7	54	PRIMARY	0.9
1193	7	40	PRIMARY	0.85
1194	7	39	SECONDARY	0.4
683	7	44	SECONDARY	0.5
1195	1	39	PRIMARY	1
666	1	41	PRIMARY	0.95
667	1	40	PRIMARY	0.7
1196	1	54	SECONDARY	0.8
1197	1	56	SECONDARY	0.3
1198	2	39	PRIMARY	1
669	2	41	PRIMARY	0.85
670	2	52	SECONDARY	0.7
1199	2	54	SECONDARY	0.5
1200	13	43	PRIMARY	1
696	13	50	PRIMARY	0.7
695	13	47	SECONDARY	0.6
1201	26	44	PRIMARY	1
727	26	49	PRIMARY	0.7
728	26	45	SECONDARY	0.5
1202	26	46	SECONDARY	0.4
1203	27	44	PRIMARY	1
730	27	49	PRIMARY	0.9
1204	27	51	SECONDARY	0.6
731	27	45	SECONDARY	0.4
1205	22	44	PRIMARY	1
716	22	45	PRIMARY	0.9
718	22	49	PRIMARY	0.6
717	22	46	SECONDARY	0.5
1206	22	54	SECONDARY	0.7
707	18	48	PRIMARY	1
706	18	50	PRIMARY	0.7
1207	18	43	SECONDARY	0.3
991	30	41	PRIMARY	0.95
992	30	40	PRIMARY	0.8
1208	30	44	SECONDARY	0.5
1209	30	48	SECONDARY	0.6
1211	563	50	PRIMARY	1
1212	563	43	SECONDARY	0.5
1213	563	48	SECONDARY	0.5
1214	564	39	PRIMARY	1
1215	564	42	SECONDARY	0.5
1216	564	41	SECONDARY	0.5
1217	564	40	SECONDARY	0.5
1218	565	52	PRIMARY	1
1223	568	39	PRIMARY	1
1224	568	41	SECONDARY	0.5
1225	568	40	SECONDARY	0.5
1187	623	40	SECONDARY	1
1188	623	39	SECONDARY	1
1125	624	49	SECONDARY	1
1126	624	57	SECONDARY	1
1226	569	52	PRIMARY	1
1231	571	43	PRIMARY	1
1232	571	48	SECONDARY	0.5
1233	571	50	SECONDARY	0.5
1234	572	50	PRIMARY	1
1235	572	52	SECONDARY	0.5
1236	572	43	SECONDARY	0.5
1237	572	48	SECONDARY	0.5
1238	573	52	PRIMARY	1
1242	577	50	PRIMARY	1
1243	577	43	SECONDARY	0.5
1244	577	48	SECONDARY	0.5
1245	578	39	PRIMARY	1
1246	578	58	SECONDARY	0.5
1247	578	56	SECONDARY	0.5
1248	578	42	SECONDARY	0.5
1249	578	41	SECONDARY	0.5
1250	578	40	SECONDARY	0.5
1251	154	58	SECONDARY	0.5
1252	579	52	PRIMARY	1
1253	580	52	PRIMARY	1
1254	581	39	PRIMARY	1
1255	581	42	SECONDARY	0.5
1256	581	41	SECONDARY	0.5
1257	581	40	SECONDARY	0.5
1258	582	52	PRIMARY	1
1259	583	40	PRIMARY	1
1262	585	52	PRIMARY	1
1263	586	58	PRIMARY	1
1264	586	56	SECONDARY	0.5
1265	587	54	PRIMARY	1
1266	587	41	SECONDARY	0.5
1267	587	40	SECONDARY	0.5
1271	589	50	PRIMARY	1
1272	589	43	SECONDARY	0.5
1273	589	48	SECONDARY	0.5
1274	590	43	PRIMARY	1
1275	590	52	SECONDARY	0.5
1276	590	48	SECONDARY	0.5
1277	590	50	SECONDARY	0.5
1282	592	43	PRIMARY	1
1283	592	52	SECONDARY	0.5
1284	592	48	SECONDARY	0.5
1285	592	50	SECONDARY	0.5
1286	593	43	PRIMARY	1
1287	593	48	SECONDARY	0.5
1288	593	50	SECONDARY	0.5
1289	179	48	SECONDARY	0.5
1290	594	52	PRIMARY	1
1291	595	52	PRIMARY	1
1292	341	58	SECONDARY	0.5
1293	596	56	PRIMARY	1
1294	596	58	SECONDARY	0.5
1295	596	42	SECONDARY	0.5
1296	596	41	SECONDARY	0.5
1297	596	40	SECONDARY	0.5
1298	596	39	SECONDARY	0.5
1301	598	52	PRIMARY	1
1304	600	40	PRIMARY	1
1305	600	42	SECONDARY	0.5
1306	600	41	SECONDARY	0.5
1307	600	54	SECONDARY	0.5
1309	602	50	PRIMARY	1
1310	602	44	SECONDARY	0.5
1311	603	43	PRIMARY	1
1312	603	48	SECONDARY	0.5
1313	603	50	SECONDARY	0.5
1317	605	43	PRIMARY	1
1318	605	52	SECONDARY	0.5
1319	605	48	SECONDARY	0.5
1320	605	50	SECONDARY	0.5
1327	608	43	PRIMARY	1
1328	608	52	SECONDARY	0.5
1329	608	48	SECONDARY	0.5
1330	608	50	SECONDARY	0.5
1334	243	48	SECONDARY	0.5
1335	610	39	PRIMARY	1
1336	611	39	PRIMARY	1
1337	611	42	SECONDARY	0.5
1338	611	40	SECONDARY	0.5
1339	612	39	PRIMARY	1
1340	612	41	SECONDARY	0.5
1341	612	40	SECONDARY	0.5
1342	269	48	SECONDARY	0.5
1343	613	52	PRIMARY	1
1344	614	52	PRIMARY	1
1345	615	52	PRIMARY	1
1346	615	48	SECONDARY	0.5
1347	616	43	PRIMARY	1
1348	616	48	SECONDARY	0.5
1349	616	50	SECONDARY	0.5
1351	287	48	SECONDARY	0.5
1352	618	39	PRIMARY	1
1353	618	42	SECONDARY	0.5
1354	618	41	SECONDARY	0.5
1355	618	40	SECONDARY	0.5
1358	620	39	PRIMARY	1
1359	620	42	SECONDARY	0.5
1360	620	41	SECONDARY	0.5
1361	620	40	SECONDARY	0.5
1362	621	50	PRIMARY	1
1363	622	39	PRIMARY	1
1364	622	42	SECONDARY	0.5
1365	622	41	SECONDARY	0.5
1366	622	40	SECONDARY	0.5
1367	622	48	SECONDARY	0.5
1368	623	41	PRIMARY	1
1369	623	40	SECONDARY	0.5
1370	623	39	SECONDARY	0.5
1371	624	44	PRIMARY	1
1372	624	49	SECONDARY	0.5
1373	624	59	SECONDARY	0.5
1374	624	48	SECONDARY	0.5
1375	625	44	PRIMARY	1
1376	625	49	SECONDARY	0.5
1377	625	59	SECONDARY	0.5
1378	625	48	SECONDARY	0.5
1379	30	40	PRIMARY	1
1380	30	42	SECONDARY	0.5
1381	30	51	SECONDARY	0.5
1382	30	41	SECONDARY	0.5
1227	27	44	PRIMARY	1
1228	27	49	SECONDARY	0.5
1229	27	51	SECONDARY	0.5
1230	27	59	SECONDARY	0.5
1314	26	44	PRIMARY	1
1315	26	49	SECONDARY	0.5
1316	26	59	SECONDARY	0.5
1331	16	43	PRIMARY	1
1332	16	48	SECONDARY	0.5
1333	16	50	SECONDARY	0.5
1387	627	40	PRIMARY	1
1388	627	51	SECONDARY	0.5
1389	627	41	SECONDARY	0.5
1390	627	54	SECONDARY	0.5
1391	627	39	SECONDARY	0.5
1392	627	45	SECONDARY	0.5
1393	628	39	PRIMARY	1
1394	628	51	SECONDARY	0.5
1395	628	41	SECONDARY	0.5
1396	628	40	SECONDARY	0.5
1397	628	54	SECONDARY	0.5
1398	628	45	SECONDARY	0.5
1399	629	45	PRIMARY	1
1400	629	51	SECONDARY	0.5
1401	629	48	SECONDARY	0.5
1410	631	39	PRIMARY	1
1411	631	42	SECONDARY	0.5
1412	631	41	SECONDARY	0.5
1413	631	40	SECONDARY	0.5
1414	631	48	SECONDARY	0.5
1415	631	45	SECONDARY	0.5
1416	632	39	PRIMARY	1
1417	632	52	SECONDARY	0.5
1418	632	42	SECONDARY	0.5
1419	632	41	SECONDARY	0.5
1420	632	40	SECONDARY	0.5
1421	633	39	PRIMARY	1
1422	633	42	SECONDARY	0.5
1423	633	51	SECONDARY	0.5
1424	633	41	SECONDARY	0.5
1425	633	40	SECONDARY	0.5
1426	633	54	SECONDARY	0.5
1427	633	48	SECONDARY	0.5
1428	633	45	SECONDARY	0.5
1429	634	39	PRIMARY	1
1430	634	42	SECONDARY	0.5
1431	634	51	SECONDARY	0.5
1432	634	41	SECONDARY	0.5
1433	634	40	SECONDARY	0.5
1434	634	54	SECONDARY	0.5
1435	634	48	SECONDARY	0.5
1436	634	45	SECONDARY	0.5
1437	635	40	PRIMARY	1
1438	635	52	SECONDARY	0.5
1439	635	42	SECONDARY	0.5
1440	635	51	SECONDARY	0.5
1441	635	41	SECONDARY	0.5
1442	635	54	SECONDARY	0.5
1443	635	39	SECONDARY	0.5
1444	635	48	SECONDARY	0.5
1445	635	45	SECONDARY	0.5
1455	637	39	PRIMARY	1
1456	637	52	SECONDARY	0.5
1457	637	51	SECONDARY	0.5
1458	637	41	SECONDARY	0.5
1459	637	40	SECONDARY	0.5
1460	637	48	SECONDARY	0.5
1461	637	50	SECONDARY	0.5
1462	638	48	PRIMARY	1
1463	638	41	SECONDARY	0.5
1464	638	40	SECONDARY	0.5
1465	638	39	SECONDARY	0.5
1466	638	50	SECONDARY	0.5
1467	639	39	PRIMARY	1
1468	639	52	SECONDARY	0.5
1469	639	42	SECONDARY	0.5
1470	640	41	PRIMARY	1
1471	640	42	SECONDARY	0.5
1472	640	40	SECONDARY	0.5
1473	640	39	SECONDARY	0.5
1474	641	40	PRIMARY	1
1475	641	41	SECONDARY	0.5
1476	641	54	SECONDARY	0.5
1477	641	39	SECONDARY	0.5
1478	641	48	SECONDARY	0.5
1479	641	50	SECONDARY	0.5
1480	642	39	PRIMARY	1
1481	642	42	SECONDARY	0.5
1482	642	41	SECONDARY	0.5
1483	642	40	SECONDARY	0.5
1484	643	39	PRIMARY	1
1485	643	52	SECONDARY	0.5
1486	643	42	SECONDARY	0.5
1487	643	41	SECONDARY	0.5
1488	643	40	SECONDARY	0.5
1489	643	54	SECONDARY	0.5
1490	643	48	SECONDARY	0.5
1491	643	50	SECONDARY	0.5
1492	644	40	PRIMARY	1
1493	644	39	SECONDARY	0.5
1494	645	39	PRIMARY	1
1495	645	52	SECONDARY	0.5
1496	645	42	SECONDARY	0.5
1497	645	41	SECONDARY	0.5
1498	645	40	SECONDARY	0.5
1499	645	48	SECONDARY	0.5
1500	645	50	SECONDARY	0.5
1501	646	40	PRIMARY	1
1502	646	42	SECONDARY	0.5
1503	646	41	SECONDARY	0.5
1504	646	54	SECONDARY	0.5
1505	646	39	SECONDARY	0.5
1506	646	48	SECONDARY	0.5
1507	646	45	SECONDARY	0.5
1508	646	50	SECONDARY	0.5
1509	647	39	PRIMARY	1
1510	647	42	SECONDARY	0.5
1511	647	51	SECONDARY	0.5
1512	647	41	SECONDARY	0.5
1513	647	40	SECONDARY	0.5
1514	647	54	SECONDARY	0.5
1515	647	48	SECONDARY	0.5
1516	647	45	SECONDARY	0.5
1517	647	50	SECONDARY	0.5
1518	648	48	PRIMARY	1
1519	648	39	SECONDARY	0.5
1520	648	50	SECONDARY	0.5
1521	649	48	PRIMARY	1
1522	649	42	SECONDARY	0.5
1523	649	39	SECONDARY	0.5
1524	649	50	SECONDARY	0.5
1533	32	39	PRIMARY	1
1534	32	49	SECONDARY	0.5
1535	32	41	SECONDARY	0.5
1402	33	48	PRIMARY	1
1403	33	52	SECONDARY	0.5
1404	33	41	SECONDARY	0.5
1405	33	40	SECONDARY	0.5
1406	33	54	SECONDARY	0.5
1407	33	39	SECONDARY	0.5
1408	33	45	SECONDARY	0.5
1525	247	48	PRIMARY	1
1526	247	51	SECONDARY	0.5
1527	247	45	SECONDARY	0.5
1547	654	40	PRIMARY	1
1548	654	51	SECONDARY	0.5
1549	654	41	SECONDARY	0.5
1550	654	40	SECONDARY	0.5
1551	654	54	SECONDARY	0.5
1552	654	39	SECONDARY	0.5
1553	654	45	SECONDARY	0.5
1554	655	45	PRIMARY	1
1555	655	51	SECONDARY	0.5
1556	655	48	SECONDARY	0.5
1557	656	39	PRIMARY	1
1558	656	42	SECONDARY	0.5
1559	656	51	SECONDARY	0.5
1560	656	41	SECONDARY	0.5
1561	656	40	SECONDARY	0.5
1562	656	54	SECONDARY	0.5
1563	656	48	SECONDARY	0.5
1564	656	45	SECONDARY	0.5
1565	656	50	SECONDARY	0.5
1566	657	39	PRIMARY	1
1567	657	42	SECONDARY	0.5
1568	657	51	SECONDARY	0.5
1569	657	41	SECONDARY	0.5
1570	657	40	SECONDARY	0.5
1571	657	54	SECONDARY	0.5
1572	657	48	SECONDARY	0.5
1573	657	45	SECONDARY	0.5
1574	658	39	PRIMARY	1
1575	658	41	SECONDARY	0.5
1576	658	40	SECONDARY	0.5
1577	658	48	SECONDARY	0.5
1578	658	50	SECONDARY	0.5
1579	659	40	PRIMARY	1
1580	659	42	SECONDARY	0.5
1581	659	51	SECONDARY	0.5
1582	659	41	SECONDARY	0.5
1583	659	40	SECONDARY	0.5
1584	659	54	SECONDARY	0.5
1585	659	39	SECONDARY	0.5
1586	659	48	SECONDARY	0.5
1587	659	45	SECONDARY	0.5
1588	659	50	SECONDARY	0.5
1594	662	43	PRIMARY	1
1595	662	48	SECONDARY	0.5
1599	666	54	PRIMARY	1
1600	666	59	SECONDARY	0.5
1601	666	45	SECONDARY	0.5
1602	120	48	SECONDARY	0.5
1603	123	59	SECONDARY	0.5
1604	667	54	PRIMARY	1
1605	667	52	SECONDARY	0.5
1606	667	58	SECONDARY	0.5
1607	667	41	SECONDARY	0.5
1608	667	40	SECONDARY	0.5
1609	667	39	SECONDARY	0.5
1610	668	54	PRIMARY	1
1611	668	58	SECONDARY	0.5
1612	668	41	SECONDARY	0.5
1613	669	43	PRIMARY	1
1614	669	59	SECONDARY	0.5
1615	335	48	SECONDARY	0.5
1616	670	42	PRIMARY	1
1617	671	56	PRIMARY	1
1618	672	40	PRIMARY	1
1619	673	58	PRIMARY	1
1620	674	58	PRIMARY	1
1622	187	58	SECONDARY	0.5
1623	676	39	PRIMARY	1
1624	676	39	SECONDARY	0.5
1626	678	40	PRIMARY	1
1627	679	54	PRIMARY	1
1628	680	40	PRIMARY	1
1629	680	42	SECONDARY	0.5
1631	682	44	PRIMARY	1
1632	683	44	PRIMARY	1
1633	683	50	SECONDARY	0.5
1634	542	43	SECONDARY	0.5
1635	542	51	SECONDARY	0.5
1636	542	44	SECONDARY	0.5
1637	542	50	SECONDARY	0.5
1638	684	42	PRIMARY	1
1639	685	42	PRIMARY	1
1641	687	42	PRIMARY	1
1642	244	48	SECONDARY	0.5
1644	689	48	PRIMARY	1
1645	689	49	SECONDARY	0.5
1646	689	43	SECONDARY	0.5
1647	690	42	PRIMARY	1
1648	690	40	SECONDARY	0.5
1649	690	54	SECONDARY	0.5
1650	691	40	PRIMARY	1
1651	691	42	SECONDARY	0.5
1652	692	40	PRIMARY	1
1653	692	42	SECONDARY	0.5
1654	693	52	PRIMARY	1
1655	694	48	PRIMARY	1
1656	694	45	SECONDARY	0.5
1657	695	48	PRIMARY	1
1658	695	44	SECONDARY	0.5
1659	696	48	PRIMARY	1
1660	697	44	PRIMARY	1
1661	698	56	PRIMARY	1
1662	698	40	SECONDARY	0.5
1663	699	48	PRIMARY	1
1664	699	51	SECONDARY	0.5
1665	699	44	SECONDARY	0.5
1666	700	39	PRIMARY	1
1667	700	58	SECONDARY	0.5
1668	700	41	SECONDARY	0.5
1669	700	40	SECONDARY	0.5
1670	701	49	PRIMARY	1
1671	701	43	SECONDARY	0.5
1672	701	48	SECONDARY	0.5
1675	703	40	PRIMARY	1
1676	704	39	PRIMARY	1
1677	705	52	PRIMARY	1
1678	706	42	PRIMARY	1
1679	707	52	PRIMARY	1
1680	708	50	PRIMARY	1
1681	708	48	SECONDARY	0.5
1687	711	48	PRIMARY	1
1688	711	43	SECONDARY	0.5
1689	711	44	SECONDARY	0.5
1383	30	54	SECONDARY	0.5
1384	30	39	SECONDARY	0.5
1385	30	48	SECONDARY	0.5
1386	30	45	SECONDARY	0.5
1536	32	40	SECONDARY	0.5
1537	32	54	SECONDARY	0.5
1538	32	48	SECONDARY	0.5
1539	32	45	SECONDARY	0.5
1540	32	50	SECONDARY	0.5
1409	33	50	SECONDARY	0.5
1589	316	40	PRIMARY	1
1590	316	56	SECONDARY	0.5
1541	546	39	PRIMARY	1
1542	546	42	SECONDARY	0.5
1543	546	41	SECONDARY	0.5
1544	546	40	SECONDARY	0.5
1591	316	41	SECONDARY	0.5
1592	316	54	SECONDARY	0.5
1545	546	48	SECONDARY	0.5
1546	546	50	SECONDARY	0.5
619	186	41	SECONDARY	1
620	186	40	SECONDARY	1
621	186	54	SECONDARY	1
672	491	41	SECONDARY	1
673	491	52	SECONDARY	1
1241	131	52	PRIMARY	1
1350	131	52	PRIMARY	1
597	389	42	SECONDARY	1
598	389	41	SECONDARY	1
599	389	39	SECONDARY	1
1643	245	39	PRIMARY	1
1640	231	41	PRIMARY	1
1684	369	40	PRIMARY	1
1685	369	54	SECONDARY	0.5
1686	369	59	SECONDARY	0.5
1593	75	42	PRIMARY	1
1598	116	42	PRIMARY	1
1596	98	49	PRIMARY	1
1625	194	44	PRIMARY	1
1014	16	43	SECONDARY	1
1015	16	57	SECONDARY	1
1016	16	57	SECONDARY	1
1017	16	50	SECONDARY	1
1268	16	43	PRIMARY	1
1269	16	48	SECONDARY	0.5
1270	16	50	SECONDARY	0.5
1278	16	43	PRIMARY	1
1279	16	52	SECONDARY	0.5
1280	16	48	SECONDARY	0.5
1281	16	50	SECONDARY	0.5
1321	16	50	PRIMARY	1
1322	16	43	SECONDARY	0.5
1323	16	48	SECONDARY	0.5
1324	16	43	PRIMARY	1
1325	16	48	SECONDARY	0.5
1326	16	50	SECONDARY	0.5
1446	635	40	PRIMARY	1
1447	635	52	SECONDARY	0.5
1448	635	42	SECONDARY	0.5
1449	635	51	SECONDARY	0.5
1450	635	41	SECONDARY	0.5
1451	635	54	SECONDARY	0.5
1452	635	39	SECONDARY	0.5
1453	635	48	SECONDARY	0.5
1454	635	45	SECONDARY	0.5
985	512	43	SECONDARY	1
986	512	40	SECONDARY	1
987	512	57	SECONDARY	1
644	383	42	SECONDARY	1
645	383	40	SECONDARY	1
1528	8	40	PRIMARY	1
1529	8	51	SECONDARY	0.5
1530	8	41	SECONDARY	0.5
1531	8	54	SECONDARY	0.5
1532	8	45	SECONDARY	0.5
613	692	42	SECONDARY	1
713	501	50	SECONDARY	1
714	501	52	SECONDARY	1
715	501	45	SECONDARY	1
1260	501	48	PRIMARY	1
1261	501	50	SECONDARY	0.5
1044	502	43	SECONDARY	1
1045	502	57	SECONDARY	1
1046	502	52	SECONDARY	1
1682	708	50	PRIMARY	1
1683	708	44	SECONDARY	0.5
\.


--
-- Data for Name: movements; Type: TABLE DATA; Schema: public; Owner: jacked
--

COPY public.movements (id, name, primary_muscle, primary_region, compound, is_complex_lift, is_unilateral, metric_type, spinal_compression, bodyweight_possible, dumbbell_possible, kettlebell_possible, barbell_possible, machine_possible, band_possible, plate_or_med_ball_possible, regression_to_move, progression_to_move, variation_to_move, discipline, pattern, pattern_subtype) FROM stdin;
633	Hang Clean	glutes	anterior lower	t	t	f	reps	high	f	f	t	t	f	f	f	\N	\N	\N	olympic	hinge	hinge
623	Step Up	glutes	posterior lower	t	f	f	reps	low	t	t	f	t	f	f	f	\N	\N	\N	resistance training	lunge	lunge
637	Heaving Snatch Balance	quadriceps	anterior lower	t	t	f	reps	high	f	f	f	t	f	f	f	\N	\N	\N	olympic	squat	squat
587	Hyperextensions With No Hyperextension Bench	lower_back	posterior lower	f	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	hinge	hinge
668	Dancer'S Stretch	lower_back	posterior lower	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	hinge	stretch
231	Piriformis-Smr	glutes	posterior lower	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	mobility	hinge	smr
631	Clean From Blocks	quadriceps	anterior lower	t	t	f	reps	high	f	f	f	t	f	f	f	\N	\N	\N	olympic	squat	hinge
700	Sit Squats	quadriceps	anterior lower	t	f	f	time	none	t	f	f	f	f	f	f	\N	\N	1	resistance training	squat	squat
632	Frankenstein Squat	quadriceps	anterior lower	t	t	f	reps	high	f	f	f	t	f	f	f	\N	\N	642	olympic	squat	squat
600	Natural Glute Ham Raise	hamstrings	posterior lower	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	hinge	hinge
578	Double Leg Butt Kick	quadriceps	anterior lower	t	f	f	reps	low	t	f	f	f	t	f	f	\N	\N	\N	athletic	squat	squat
230	Pin Presses	triceps	posterior upper	f	f	f	reps	none	f	f	f	t	f	f	f	\N	\N	125	resistance training	horizontal_push	horizontal_push
654	Snatch Deadlift	hamstrings	posterior lower	t	t	f	reps	high	f	f	f	t	f	f	f	\N	\N	627	olympic	hinge	hinge
337	Floor Press With Chains	triceps	posterior upper	f	f	f	reps	none	f	f	f	t	f	f	f	\N	\N	125	resistance training	horizontal_push	horizontal_push
171	Inchworm	hamstrings	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	hinge	hinge
66	90/90 Hamstring	hamstrings	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	hinge	hinge
602	Overhead Triceps	triceps	anterior upper	f	f	f	time	low	t	f	f	f	f	f	f	\N	\N	\N	mobility	horizontal_push	horizontal_push
708	Tricep Side Stretch	triceps	anterior upper	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	horizontal_push	stretch
655	Snatch Shrug	upper_back	posterior upper	f	t	f	reps	high	f	f	f	t	f	f	f	\N	\N	\N	olympic	horizontal_pull	horizontal_pull
160	Glute Kickback	glutes	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	hinge	hinge
672	Hamstring Smr	hamstrings	posterior lower	f	f	f	time	none	f	f	f	f	f	f	f	\N	\N	\N	mobility	hinge	smr
659	Split Snatch	hamstrings	posterior lower	t	t	f	reps	high	f	f	f	t	f	f	f	\N	\N	\N	olympic	hinge	hinge
657	Split Clean	glutes	anterior lower	t	t	f	reps	high	f	t	t	t	f	f	f	\N	\N	\N	olympic	hinge	hinge
658	Split Jerk	glutes	anterior lower	t	t	f	reps	high	f	f	f	t	f	f	f	\N	\N	\N	olympic	hinge	hinge
123	Child'S Pose	lower_back	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	hinge	hinge
329	Box Skip	hamstrings	posterior lower	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	resistance training	lunge	lunge
101	Butt Lift (Bridge)	glutes	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	lunge	lunge
333	Dumbbell Lunges	quadriceps	anterior lower	t	f	f	reps	none	f	t	f	f	f	f	f	\N	\N	6	resistance training	lunge	lunge
346	Lunge Pass Through	hamstrings	posterior lower	t	f	f	reps	none	f	f	t	f	f	f	f	\N	\N	\N	resistance training	lunge	lunge
48	Tricep Extension	triceps	posterior upper	f	f	f	reps	none	f	t	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
621	Standing Towel Triceps Extension	triceps	anterior upper	f	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
411	Ring Push Ups	full_body	full body	t	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
340	Kettlebell Sumo High Pull	upper_back	posterior upper	f	f	f	reps	none	f	f	t	f	f	f	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
359	Seated Two-Arm Palms-Up Low-Pulley Wrist Curl	forearms	anterior upper	f	f	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
251	Reverse Barbell Preacher Curls	biceps	anterior upper	f	f	f	reps	none	f	f	f	t	f	f	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
581	Freehand Jump Squat	quadriceps	anterior lower	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	1	resistance training	squat	plyometric
564	Bench Jump	quadriceps	anterior lower	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	athletic	squat	plyometric
611	Rocket Jump	quadriceps	anterior lower	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	athletic	squat	plyometric
612	Scissors Jump	quadriceps	anterior lower	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	athletic	squat	plyometric
534	Jumping Lunge	quadriceps	anterior lower	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	athletic	lunge	plyometric
179	Isometric Wipers	chest	anterior upper	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_push	isometric
528	Quad Stretch	quadriceps	anterior lower	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	stretch	squat	stretch
691	Seated Floor Hamstring Stretch	hamstrings	posterior lower	t	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	hinge	stretch
692	Seated Hamstring And Calf Stretch	hamstrings	posterior lower	t	f	f	time	none	f	f	f	f	f	f	f	\N	\N	\N	stretch	hinge	stretch
356	Runner'S Stretch	hamstrings	posterior lower	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	hinge	stretch
371	World'S Greatest Stretch	hamstrings	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	hinge	stretch
339	Intermediate Groin Stretch	hamstrings	posterior lower	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	stretch	hinge	stretch
703	Standing Hamstring And Calf Stretch	hamstrings	posterior lower	t	f	f	time	none	f	f	f	f	f	f	f	\N	\N	\N	stretch	hinge	stretch
543	Doorway Stretch	chest	upper body	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	stretch	horizontal_push	stretch
510	Hammer Curl	biceps	anterior upper	f	f	t	reps	low	f	t	t	f	t	t	t	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
47	Bicep Curl	biceps	anterior upper	f	f	f	reps	none	f	t	t	t	t	t	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
338	Heavy Bag Thrust	chest	anterior upper	t	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
502	Strict Ring Dips	chest	anterior upper	t	f	f	reps	none	t	f	f	f	f	f	t	\N	\N	\N	crossfit	horizontal_push	horizontal_push
593	Isometric Chest Squeezes	chest	anterior upper	f	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	athletic	horizontal_push	isometric
634	Hang Clean Below The Knees	quadriceps	anterior lower	t	t	f	reps	high	f	f	f	t	f	f	f	\N	\N	\N	olympic	squat	squat
635	Hang Snatch	glutes	posterior lower	t	t	f	reps	high	f	f	t	t	f	f	f	\N	\N	\N	olympic	hinge	hinge
314	Weighted Sit-Ups-With Bands	core	full body	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	resistance training	core	core
648	Push Press	side_delts	shoulder	f	t	f	reps	high	f	f	f	t	f	f	f	\N	\N	649	olympic	vertical_push	vertical_push
711	Upward Stretch	side_delts	shoulder	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	vertical_push	stretch
594	Jackknife Sit Up	core	core	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	core	core
256	Reverse Hyperextension	hamstrings	posterior lower	f	f	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	hinge	hinge
312	Weighted Ball Hyperextension	lower_back	posterior lower	f	f	f	reps	none	f	f	f	f	f	f	t	\N	\N	\N	resistance training	hinge	hinge
228	Pelvic Tilt Into Bridge	lower_back	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	hinge	hinge
56	Cat-Cow	lower_back	posterior upper	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	hinge	hinge
248	Rack Pulls	lower_back	posterior lower	f	f	f	reps	none	f	f	f	t	f	f	f	\N	\N	\N	resistance training	hinge	hinge
227	One Knee To Chest	glutes	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	hinge	hinge
298	Straight-Arm Dumbbell Pullover	chest	anterior upper	f	f	f	reps	none	f	t	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
363	Speed Band Overhead Triceps	triceps	posterior upper	f	f	f	reps	none	f	f	f	f	f	t	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
572	Close Grip Push Up Off Of A Dumbbell	triceps	anterior upper	f	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	vertical_push	vertical_push
273	Seated One-Arm Cable Pulley Rows	full_body	posterior upper	t	f	f	time	none	f	f	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
255	Reverse Grip Bent-Over Rows	full_body	full body	t	f	f	time	none	f	f	f	t	f	f	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
24	Seated Cable Row	lats	posterior upper	t	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	22	resistance training	horizontal_pull	horizontal_pull
25	Inverted Row	upper_back	posterior upper	t	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
577	Dips Triceps Version	triceps	anterior upper	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	vertical_push	vertical_push
589	Incline Push Up Close Grip	triceps	anterior upper	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	vertical_push	vertical_push
592	Incline Push Up Wide	chest	anterior upper	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	vertical_push	vertical_push
245	Quadriceps-Smr	quadriceps	anterior lower	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	mobility	squat	smr
638	Jerk Balance	side_delts	shoulder	t	t	f	reps	high	f	f	f	t	f	f	f	\N	\N	\N	olympic	vertical_push	vertical_push
188	Knee Circles	calves	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	mobility	mobility
49	Lateral Raise	side_delts	shoulder	f	f	f	reps	none	f	t	f	f	f	f	f	\N	\N	\N	resistance training	vertical_push	vertical_push
293	Standing Pelvic Tilt	lower_back	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	hinge	stretch
649	Push Press Behind The Neck	side_delts	shoulder	t	t	f	reps	high	f	f	f	t	f	f	f	\N	\N	648	resistance training	vertical_push	vertical_push
712	Burpee Broad Jumps	quadriceps	full body	\N	\N	\N	reps	none	t	f	f	f	f	f	f	\N	\N	\N	crossfit	conditioning	\N
563	Bench Dips	triceps	anterior upper	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	vertical_push	vertical_push
713	Calorie Ski Erg	full_body	full body	\N	\N	\N	calories	none	f	f	f	f	t	f	f	\N	\N	\N	cardio	conditioning	\N
295	Standing Two-Arm Overhead Throw	full_body	shoulder	t	f	f	time	none	f	f	f	f	f	f	t	\N	\N	\N	resistance training	vertical_push	vertical_push
714	V-Ups	core	core	\N	\N	\N	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	core	\N
565	Bent Knee Hip Raise	core	core	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	rotation	rotation
569	Butt Ups	core	core	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	rotation	rotation
573	Cocoons	core	core	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	rotation	rotation
407	Knees To Elbows	hip_flexors	core	t	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	resistance training	rotation	rotation
715	Sit-Ups	core	core	\N	\N	\N	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	core	\N
192	Landmine 180'S	core	full body	f	f	f	reps	none	f	f	f	t	f	f	f	\N	\N	\N	resistance training	carry	carry
328	Bottoms Up	core	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	carry	carry
350	Otis-Up	core	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	carry	carry
345	Lower Back Curl	core	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	carry	carry
716	Sandbag Lunges	quadriceps	lower body	\N	\N	\N	reps	none	f	f	f	f	f	f	t	\N	\N	\N	resistance training	lunge	\N
717	Lunges	quadriceps	lower body	\N	\N	\N	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	lunge	\N
72	Alternate Heel Touchers	core	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	carry	carry
246	Quick Leap	quadriceps	anterior lower	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	athletic	squat	plyometric
122	Chest Stretch On Stability Ball	chest	anterior upper	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	stretch	horizontal_push	stretch
120	Chest And Front Of Shoulder Stretch	chest	anterior upper	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	stretch	horizontal_push	stretch
527	Lat Stretch	lats	posterior upper	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	stretch	horizontal_pull	stretch
365	Standing Elevated Quad Stretch	quadriceps	anterior lower	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	stretch	squat	stretch
324	All Fours Quad Stretch	quadriceps	anterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	squat	stretch
701	Standing Biceps Stretch	biceps	anterior upper	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	horizontal_pull	stretch
243	Pushups (Close And Wide Hand Positions)	chest	anterior upper	f	f	f	reps	none	t	f	f	f	f	t	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
669	Dynamic Chest Stretch	chest	anterior upper	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	horizontal_push	dynamic_warmup
605	Push Up Wide	chest	anterior upper	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	vertical_push	horizontal_push
616	Single Arm Push Up	chest	anterior upper	t	t	t	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
590	Incline Push Up Medium	chest	anterior upper	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
571	Clock Push Up	chest	anterior upper	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
608	Push Up To Side Plank	chest	anterior upper	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
16	Push-Up	chest	anterior upper	t	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
360	Side Jackknife	core	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	carry	rotation
585	Hanging Pike	core	core	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	vertical_push	vertical_push
302	Supine Two-Arm Overhead Throw	core	shoulder	f	f	f	time	none	f	f	f	f	f	f	t	\N	\N	301	resistance training	vertical_push	vertical_push
277	Single-Cone Sprint Drill	quadriceps	anterior lower	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	athletic	squat	squat
647	Power Snatch From Blocks	quadriceps	anterior lower	t	t	f	reps	high	f	f	f	t	f	f	f	\N	\N	\N	olympic	squat	squat
656	Snatch From Blocks	quadriceps	anterior lower	t	t	f	reps	high	f	f	f	t	f	f	f	\N	\N	\N	olympic	squat	squat
491	Kettlebell Goblet Squats	quadriceps	lower body	t	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	376	resistance training	squat	squat
364	Split Squats	hamstrings	posterior lower	t	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	squat	squat
216	Oblique Crunches	obliques	full body	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	core	core
12	Kettlebell Swing	glutes	posterior lower	t	f	f	reps	none	f	f	t	f	f	f	f	\N	\N	\N	resistance training	hinge	hinge
509	Deficit Deadlift	glutes	posterior lower	t	f	f	reps	low	f	f	f	t	f	f	f	\N	\N	7	resistance training	hinge	hinge
313	Weighted Crunches	core	full body	f	f	f	time	none	f	f	f	f	f	f	t	\N	\N	\N	resistance training	core	core
134	Decline Crunch	core	core	f	f	f	time	none	f	f	f	f	f	f	f	\N	\N	\N	resistance training	core	core
136	Decline Oblique Crunch	core	full body	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	core	core
137	Decline Reverse Crunch	core	full body	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	core	core
212	Monster Walk	adductors	lower body	f	f	f	reps	none	f	f	f	f	f	t	f	\N	\N	\N	resistance training	carry	carry
247	Rack Delivery	full_body	full body	f	f	f	reps	none	f	f	f	t	f	f	f	\N	\N	\N	resistance training	carry	carry
257	Reverse Machine Flyes	full_body	full body	f	f	f	reps	none	f	f	f	f	t	f	f	253	\N	\N	resistance training	carry	carry
250	Return Push From Stance	full_body	full body	f	f	f	reps	none	f	f	f	f	f	f	t	\N	\N	\N	resistance training	carry	carry
68	Adductor	adductors	lower body	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	mobility	carry	carry
161	Gorilla Chin/Crunch	core	full body	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	core	core
304	Suspended Reverse Crunch	lower_back	full body	f	f	f	time	none	f	f	f	f	f	f	f	\N	\N	\N	resistance training	core	core
162	Groiners	adductors	lower body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	carry	carry
215	Neck-Smr	full_body	full body	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	mobility	carry	smr
259	Rhomboids-Smr	full_body	full body	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	mobility	carry	smr
39	Dead Bug	core	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	carry	carry
684	Peroneals Smr	calves	posterior lower	f	f	f	time	none	f	f	f	f	f	f	f	\N	\N	\N	stretch	carry	smr
679	Lower Back Smr	lower_back	posterior lower	f	f	f	time	none	f	f	f	f	f	f	f	\N	\N	\N	mobility	hinge	smr
586	Hip Circles (Prone)	full_body	posterior lower	f	f	f	time	low	t	f	f	f	f	f	f	\N	\N	\N	mobility	mobility	mobility
521	Cardio Intervals	full_body	full body	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	cardio	carry	carry
522	Foam Rolling	full_body	full body	f	f	f	reps	low	f	f	f	f	f	f	f	\N	\N	\N	stretch	carry	foam_roll
204	Lying Crossover	adductors	lower body	f	f	t	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	carry	carry
7	Conventional Deadlift	glutes	posterior lower	t	t	f	reps	moderate	f	f	f	t	f	f	f	\N	\N	8	resistance training	hinge	hinge
266	Sandbag Load	quadriceps	anterior lower	f	f	f	reps	none	f	f	f	f	f	f	t	\N	\N	\N	cardio	carry	farmer_carry
61	Wall Sit	quadriceps	anterior lower	t	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	athletic	squat	isometric
376	Air Squat	quadriceps	lower body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	500	crossfit	squat	squat
1	Back Squat	quadriceps	anterior lower	t	t	f	reps	none	f	f	f	t	f	f	f	\N	\N	2	resistance training	squat	squat
402	Chest To Bar Pull Ups	full_body	full body	t	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	resistance training	vertical_pull	vertical_pull
515	Upright Row	side_delts	shoulder	t	f	f	reps	low	f	f	f	t	f	f	f	\N	\N	\N	resistance training	vertical_pull	vertical_pull
28	Lat Pulldown	lats	posterior upper	t	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	resistance training	vertical_pull	vertical_pull
680	Lying Hamstring	hamstrings	posterior lower	t	f	f	time	none	f	f	f	f	f	f	f	\N	\N	\N	mobility	hinge	hinge
676	Kneeling Hip Flexor	hip_flexors	anterior lower	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	squat	squat
683	Overhead Lat	lats	posterior upper	t	f	f	time	none	f	f	f	f	f	f	f	\N	\N	\N	mobility	horizontal_pull	horizontal_pull
699	Side Wrist Pull	side_delts	shoulder	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	vertical_push	vertical_push
674	Iliotibial Tract Smr	full_body	posterior lower	f	f	f	time	none	f	f	f	f	f	f	f	\N	\N	\N	mobility	carry	smr
678	Leg Up Hamstring Stretch	hamstrings	posterior lower	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	hinge	stretch
533	Jumping Jacks	full_body	full body	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	athletic	carry	plyometric
307	Thigh Adductor	adductors	lower body	f	f	f	reps	none	t	f	f	f	t	t	f	\N	\N	\N	resistance training	carry	carry
671	Groin And Back Stretch	adductors	posterior lower	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	carry	stretch
595	Janda Sit Up	core	core	f	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	core	core
670	Foot Smr	calves	posterior lower	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	carry	smr
42	Ab Wheel Rollout	core	anterior upper	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	carry	carry
151	Elbow To Knee	hip_flexors	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	carry	carry
287	Spider Crawl	core	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	carry	bear_crawl
64	Battle Rope Wave	core	full body	t	f	f	time	none	f	f	f	f	f	f	f	\N	\N	\N	crossfit	rotation	rotation
31	Power Clean	full_body	full body	t	t	f	reps	none	f	f	f	t	f	f	f	\N	\N	\N	olympic	hinge	hinge
32	Snatch	full_body	full body	t	t	f	reps	none	f	f	f	t	f	f	f	\N	\N	\N	olympic	hinge	hinge
400	Rowing Machine	full_body	full body	f	f	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	cardio	carry	row
583	Front Leg Raises	hip_flexors	core	t	f	f	time	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	rotation	rotation
615	Side Bridge	core	core	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	rotation	rotation
610	Rear Leg Raises	hip_flexors	anterior lower	t	f	f	time	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	rotation	rotation
613	Seated Flat Bench Leg Pull In	hip_flexors	core	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	rotation	rotation
268	Seated Barbell Twist	core	full body	f	f	f	reps	none	f	f	f	t	f	f	f	\N	\N	\N	resistance training	rotation	rotation
174	Incline Dumbbell Flyes-With A Twist	chest	anterior upper	f	f	f	reps	none	f	t	f	f	f	f	f	\N	\N	\N	resistance training	rotation	rotation
265	Russian Twist	core	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	rotation	rotation
598	Leg Pull In	hip_flexors	core	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	rotation	rotation
41	Hanging Leg Raise	hip_flexors	core	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	resistance training	carry	carry
306	Thigh Abductor	abductors	lower body	f	f	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	carry	carry
279	Single Leg Glute Bridge	glutes	posterior lower	f	f	t	reps	none	t	t	f	t	t	f	f	\N	\N	\N	resistance training	hinge	hinge
11	Good Morning	hamstrings	posterior lower	t	f	f	reps	none	f	f	f	t	f	f	f	\N	\N	\N	resistance training	hinge	hinge
275	Single-Arm Cable Crossover	chest	anterior upper	f	f	t	reps	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
14	Incline Bench Press	chest	anterior upper	t	f	f	reps	none	f	t	f	t	f	f	f	\N	\N	13	resistance training	horizontal_push	horizontal_push
23	Single Arm Row	lats	posterior upper	t	f	t	reps	none	f	t	t	f	f	f	f	\N	\N	22	resistance training	horizontal_pull	horizontal_pull
276	Single-Arm Linear Jammer	full_body	full body	f	f	t	reps	none	f	f	f	t	f	f	f	\N	\N	\N	resistance training	carry	carry
55	Pigeon Stretch	glutes	posterior lower	f	f	t	time	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	hinge	stretch
285	Smith Machine One-Arm Upright Row	full_body	full body	t	f	f	time	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	carry	carry
568	Squat	quadriceps	anterior lower	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	1	resistance training	squat	squat
666	Cat Stretch	lower_back	posterior lower	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	hinge	stretch
622	Star Jump	quadriceps	anterior lower	f	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	athletic	squat	plyometric
620	Standing Long Jump	quadriceps	anterior lower	f	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	athletic	squat	plyometric
618	Split Jump	quadriceps	anterior lower	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	athletic	squat	plyometric
582	Frog Sit Ups	core	core	f	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	core	core
214	Moving Claw Series	hamstrings	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	lunge	lunge
234	Platform Hamstring Slides	hamstrings	posterior lower	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	resistance training	lunge	lunge
236	Prone Manual Hamstring	hamstrings	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	lunge	lunge
258	Reverse Plate Curls	biceps	anterior upper	f	f	f	reps	none	f	f	f	f	f	f	t	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
292	Standing Olympic Plate Hand Squeeze	forearms	anterior upper	f	f	f	reps	none	f	f	f	f	f	f	t	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
284	Smith Machine Behind The Back Shrug	upper_back	posterior upper	f	f	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
274	Side To Side Chins	lats	posterior upper	f	f	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
233	Plate Twist	core	full body	f	f	f	reps	none	f	f	f	f	f	f	t	\N	\N	\N	resistance training	rotation	rotation
580	Flat Bench Lying Leg Raise	core	core	f	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	carry	carry
211	Mixed Grip Chin	full_body	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	carry	carry
283	Sledgehammer Swings	core	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	carry	carry
303	Suspended Fallout	core	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	carry	carry
272	Seated Head Harness Neck Resistance	full_body	full body	f	f	f	reps	none	f	f	f	f	f	f	t	\N	\N	\N	resistance training	carry	carry
282	Sled Reverse Flye	full_body	full body	f	f	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	carry	carry
290	Standing Cable Lift	core	full body	f	f	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	carry	carry
291	Standing Cable Wood Chop	core	full body	f	f	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	carry	plyometric
249	Recumbent Bike	quadriceps	anterior lower	f	f	f	time	none	f	f	f	f	t	f	f	\N	\N	\N	cardio	squat	bike
326	Band Hip Adductions	adductors	lower body	f	f	t	reps	none	f	f	f	f	f	t	f	\N	\N	\N	resistance training	carry	carry
343	Lateral Cone Hops	adductors	lower body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	athletic	carry	plyometric
315	Wide-Grip Decline Barbell Pullover	chest	anterior upper	f	f	f	reps	none	f	f	f	t	t	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
209	Lying Prone Quadriceps	quadriceps	anterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	squat	squat
252	Reverse Crunch	core	full body	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	core	core
225	One Half Locust	quadriceps	anterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	squat	squat
165	Hug A Ball	lower_back	posterior lower	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	stretch	hinge	hinge
166	Hug Knees To Chest	lower_back	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	hinge	hinge
270	Seated Glute	glutes	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	hinge	hinge
74	Ankle On The Knee	glutes	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	hinge	hinge
187	Knee Across The Body	glutes	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	hinge	hinge
76	Arm Circles	full_body	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	mobility	mobility
200	Looking At Ceiling	upper_back	shoulder	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	mobility	stretch
226	One Handed Hang	lats	posterior upper	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	mobility	horizontal_pull	horizontal_pull
297	Stomach Vacuum	core	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	carry	carry
267	Scissor Kick	core	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	carry	carry
358	Seated Front Deltoid	full_body	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	carry	carry
341	Knee Tuck Jump	hamstrings	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	athletic	hinge	plyometric
389	Run	hamstrings	posterior lower	t	f	f	distance	none	f	f	f	f	f	f	f	\N	\N	\N	cardio	hinge	run
342	Kneeling Forearm Stretch	forearms	anterior upper	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	horizontal_pull	stretch
202	Lying Bent Leg Groin	adductors	lower body	f	f	f	reps	none	t	f	f	f	f	t	f	\N	\N	\N	mobility	carry	carry
269	Seated Biceps	biceps	anterior upper	f	f	f	reps	none	f	t	f	t	t	f	f	\N	\N	\N	mobility	horizontal_pull	horizontal_pull
335	Elbows Back	chest	anterior upper	f	f	f	reps	none	t	f	f	f	f	f	t	\N	\N	\N	stretch	horizontal_push	horizontal_push
372	Calorie Row	lats	upper body	t	f	f	reps	none	f	f	f	f	t	f	f	22	\N	\N	crossfit	horizontal_pull	horizontal_pull
673	It Band And Glute Stretch	full_body	posterior lower	f	f	f	time	none	f	f	f	f	f	f	f	\N	\N	\N	stretch	carry	stretch
110	Cable Rope Rear-Delt Rows	rear_delts	shoulder	f	f	f	time	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
65	Turkish Get-Up	full_body	full body	t	f	t	reps	none	f	t	t	f	f	f	f	\N	\N	\N	mobility	carry	turkish_get_up
301	Supine One-Arm Overhead Throw	core	shoulder	f	f	f	time	none	f	f	f	f	f	f	t	\N	\N	302	resistance training	vertical_push	vertical_push
305	The Straddle	hamstrings	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	hinge	hinge
29	Muscle-Up	lats	posterior upper	t	t	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	vertical_pull	vertical_pull
614	Seated Leg Tucks	hip_flexors	core	f	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	carry	carry
33	Clean and Jerk	full_body	posterior lower	t	t	f	reps	none	f	f	f	t	f	f	f	\N	\N	\N	crossfit	hinge	hinge
695	Shoulder Raise	side_delts	shoulder	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	vertical_push	vertical_push
579	Flat Bench Leg Pull In	hip_flexors	core	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	rotation	rotation
332	Chair Upper Body Stretch	full_body	full body	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	stretch	carry	stretch
347	Middle Back Stretch	full_body	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	carry	stretch
62	Sprint	hamstrings	posterior lower	t	f	f	distance	none	t	f	f	f	f	f	f	\N	\N	\N	athletic	hinge	hinge
142	Downward Facing Balance	glutes	posterior lower	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	mobility	hinge	hinge
71	Calorie Echo Bike	core	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	cardio	carry	carry
281	Sled Drag-Harness	quadriceps	anterior lower	f	f	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	cardio	carry	sled_drag
89	Bear Crawl Sled Drags	hamstrings	anterior lower	f	f	f	reps	none	f	f	f	f	f	f	t	\N	\N	\N	cardio	carry	bear_crawl
334	Dynamic Back Stretch	lats	posterior upper	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	horizontal_pull	dynamic_warmup
6	Walking Lunge	quadriceps	anterior lower	t	f	t	reps	none	t	t	t	t	f	f	t	\N	\N	333	resistance training	lunge	lunge
180	Jogging, Treadmill	quadriceps	anterior lower	f	f	f	time	none	f	f	f	f	t	f	f	\N	\N	\N	cardio	squat	squat
152	Elliptical Trainer	quadriceps	anterior lower	f	f	f	time	none	f	f	f	f	t	f	f	\N	\N	\N	cardio	lunge	lunge
46	Medicine Ball Slam	core	full body	t	f	f	reps	none	f	f	f	f	f	f	t	\N	\N	\N	athletic	rotation	rotation
45	Depth Jump	quadriceps	anterior lower	t	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	athletic	squat	plyometric
44	Broad Jump	glutes	posterior lower	t	f	f	distance	none	t	f	f	f	f	f	f	\N	\N	\N	athletic	hinge	plyometric
235	Plyo Kettlebell Pushups	chest	anterior upper	t	f	f	reps	none	f	f	t	f	f	f	f	\N	\N	\N	athletic	horizontal_push	plyometric
289	Stairmaster	quadriceps	anterior lower	f	f	f	time	none	f	f	f	f	t	f	f	\N	\N	\N	cardio	squat	squat
377	Back-Rack Barbell Carry	full_body	full body	t	t	f	reps	none	f	f	f	t	f	f	f	\N	\N	\N	crossfit	carry	farmer_carry
296	Step Mill	quadriceps	anterior lower	f	f	f	time	none	f	f	f	f	t	f	f	\N	\N	\N	cardio	lunge	lunge
381	Candlestick Rocks	full_body	full body	t	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	crossfit	carry	carry
523	Mobility For Lower Back	lower_back	posterior lower	f	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	mobility	hinge	hinge
57	Thoracic Rotation	upper_back	posterior upper	f	f	t	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	rotation	activation
531	High Rep Push-Up	chest	anterior upper	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
535	Pause Squat	quadriceps	anterior lower	t	f	f	reps	low	f	f	f	t	f	f	f	\N	\N	1	resistance training	squat	squat
536	Reverse Fly	rear_delts	shoulder	f	f	f	reps	low	f	t	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
546	Snatch Balance	quadriceps	anterior lower	t	t	f	reps	low	f	f	f	t	f	f	f	\N	\N	\N	olympic	hinge	hinge
529	Leg Swings	hip_flexors	anterior lower	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	mobility	hinge	hinge
547	Tall Clean	glutes	anterior lower	t	t	f	reps	low	f	f	f	f	f	f	f	\N	\N	\N	olympic	hinge	hinge
544	One-Arm Kettlebell Military Press To The Side	side_delts	shoulder	f	f	f	reps	low	f	f	t	f	f	f	f	\N	\N	\N	resistance training	vertical_push	vertical_push
348	On-Your-Back Quad Stretch	quadriceps	anterior lower	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	stretch	squat	stretch
524	Calf Stretch	calves	posterior lower	f	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	stretch	carry	stretch
525	Chest Stretch	chest	anterior upper	f	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	stretch	horizontal_push	stretch
40	Pallof Press	core	anterior upper	f	f	t	reps	none	f	f	f	f	f	t	f	\N	\N	\N	resistance training	rotation	anti_rotation
548	Tuck Planche	front_delts	anterior upper	t	t	f	time	low	f	f	f	f	f	f	f	\N	\N	\N	athletic	vertical_push	vertical_push
549	Straddle Planche	front_delts	anterior upper	t	t	f	time	low	f	f	f	f	f	f	f	\N	\N	\N	athletic	vertical_push	isometric
545	Rest	full_body	full body	f	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	mobility	carry	carry
559	Hamstring Pails/Rails	hamstrings	posterior lower	t	f	f	time	low	f	f	f	f	f	f	f	\N	\N	\N	mobility	hinge	hinge
196	Linear 3-Part Start Technique	hamstrings	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	crossfit	hinge	hinge
13	Bench Press	chest	anterior upper	t	f	f	reps	none	f	t	f	t	t	f	f	\N	\N	508	resistance training	horizontal_push	horizontal_push
22	Barbell Row	lats	posterior upper	t	f	f	reps	none	f	f	f	t	t	f	f	\N	372	23	resistance training	horizontal_pull	horizontal_pull
26	Pull-Up	lats	posterior upper	t	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	27	resistance training	vertical_pull	vertical_pull
557	Hip Pails/Rails	hip_flexors	anterior lower	t	f	f	time	low	f	f	f	f	f	f	f	\N	\N	\N	mobility	rotation	rotation
18	Overhead Press	front_delts	shoulder	t	t	f	reps	none	t	t	t	t	t	f	f	\N	\N	19	resistance training	vertical_push	vertical_push
370	Upper Back Stretch	full_body	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	carry	stretch
4	Pistol Squat	quadriceps	anterior lower	f	t	t	reps	none	t	f	f	f	f	f	f	\N	\N	1	mobility	squat	squat
560	Thoracic Pails/Rails	upper_back	posterior upper	f	f	f	time	low	f	f	f	f	f	f	f	\N	\N	\N	mobility	horizontal_pull	horizontal_pull
30	Clean	full_body	full body	t	t	f	reps	none	f	f	f	t	f	f	f	\N	\N	\N	olympic	hinge	hinge
5	Bulgarian Split Squat	quadriceps	anterior lower	t	f	t	reps	none	t	t	f	t	f	f	f	\N	\N	\N	resistance training	lunge	lunge
27	Chin-Up	lats	posterior upper	t	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	vertical_pull	vertical_pull
43	Box Jump	quadriceps	anterior lower	t	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	athletic	squat	plyometric
104	Cable Deadlifts	glutes	anterior lower	t	t	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	hinge	hinge
17	Dip	chest	anterior upper	t	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
19	Dumbbell Shoulder Press	front_delts	shoulder	t	t	f	reps	none	t	t	f	f	f	f	f	\N	\N	18	resistance training	vertical_push	vertical_push
103	Cable Crunch	core	full body	f	f	f	time	none	f	f	f	f	t	f	f	\N	\N	67	resistance training	core	core
109	Cable Reverse Crunch	core	full body	f	f	f	time	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	core	core
379	Burpees	full_body	full body	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	athletic	carry	burpee
704	Standing Hip Flexors	quadriceps	anterior lower	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	lunge	stretch
20	Pike Push-Up	front_delts	shoulder	t	t	f	reps	none	t	f	f	f	f	f	f	\N	21	\N	resistance training	vertical_push	vertical_push
38	Side Plank	obliques	anterior upper	f	f	t	time	none	t	f	f	f	f	f	f	\N	\N	\N	athletic	rotation	rotation
34	Farmer'S Carry	full_body	full body	t	f	f	distance	none	f	t	t	t	f	f	f	\N	\N	35	cardio	carry	farmer_carry
35	Offset Suitcase Carry	obliques	full body	t	f	t	distance	none	f	t	t	f	f	f	f	\N	\N	\N	cardio	carry	suitcase_carry
705	Standing Lateral Stretch	core	core	t	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	rotation	stretch
706	Standing Soleus And Achilles Stretch	calves	posterior lower	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	carry	stretch
59	L-Sit Hold	core	anterior upper	t	t	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	athletic	rotation	isometric
36	Overhead Carry	front_delts	full body	t	f	f	distance	none	f	t	t	t	f	f	f	\N	\N	\N	cardio	carry	farmer_carry
63	Sled Push	quadriceps	anterior lower	t	f	f	distance	none	f	f	f	f	f	f	t	\N	\N	\N	cardio	carry	sled_push
408	Wall Ball	full_body	full body	t	f	f	reps	none	f	f	f	f	f	f	t	\N	\N	\N	resistance training	squat	squat
93	Bicycling	quadriceps	anterior lower	f	f	f	time	none	f	f	f	f	f	f	f	\N	\N	\N	cardio	squat	squat
60	Front Lever Hold	lats	posterior upper	t	t	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	athletic	horizontal_pull	isometric
95	Bodyweight Flyes	chest	anterior upper	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
77	Around The Worlds	obliques	anterior upper	f	f	f	reps	none	f	t	t	f	f	f	f	\N	\N	\N	resistance training	rotation	rotation
308	Tire Flip	hamstrings	anterior lower	f	f	f	reps	none	f	f	f	f	f	f	t	\N	\N	\N	crossfit	hinge	hinge
143	Dumbbell Flyes	chest	anterior upper	f	f	f	reps	none	f	t	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
119	Catch And Overhead Throw	lats	posterior upper	t	f	f	time	none	f	f	f	f	f	f	t	\N	\N	22	resistance training	horizontal_pull	horizontal_pull
412	Sandbag Carry	full_body	full body	t	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	cardio	carry	carry
130	Crucifix	full_body	full body	f	f	f	reps	none	f	t	t	f	f	f	t	\N	\N	\N	resistance training	carry	carry
175	Iron Cross	full_body	full body	f	f	f	reps	none	f	t	f	f	f	f	f	\N	106	\N	resistance training	carry	carry
177	Isometric Neck Exercise-Front And Back	full_body	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	carry	isometric
118	Carioca Quick Step	adductors	lower body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	athletic	lunge	lunge
154	Fast Skipping	calves	anterior lower	f	f	f	reps	none	t	f	f	f	f	\N	f	\N	\N	\N	athletic	carry	plyometric
51	Calf Raise	calves	anterior lower	f	f	f	reps	none	t	t	f	f	t	f	f	\N	\N	\N	resistance training	squat	carry
156	Flutter Kicks	hip_flexors	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	carry	carry
183	Kettlebell Pass Between The Legs	core	full body	f	f	f	reps	none	f	f	t	f	f	f	f	\N	\N	\N	resistance training	carry	carry
199	London Bridges	lats	posterior upper	f	f	f	reps	none	f	f	f	f	f	f	t	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
398	Ghd Sit Ups	core	full body	t	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	resistance training	core	core
198	Log Lift	full_body	full body	t	t	f	reps	none	f	f	f	f	f	f	t	\N	\N	\N	olympic	carry	carry
261	Rope Climb	full_body	posterior upper	t	t	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	carry	carry
54	Hip Flexor Stretch	hip_flexors	anterior lower	f	f	t	time	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	carry	stretch
406	Kettlebell Turkish Get Ups	full_body	full body	t	f	t	reps	none	f	f	t	f	f	f	f	\N	\N	\N	crossfit	carry	turkish_get_up
435	Alternating Dumbbell Snatches	hamstrings	posterior lower	t	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	resistance training	hinge	hinge
241	Push Press-Behind The Neck	full_body	full body	t	t	f	reps	none	f	f	f	t	f	f	f	\N	\N	99	olympic	vertical_push	vertical_push
685	Peroneals Stretch	calves	posterior lower	f	f	f	time	none	f	f	f	f	f	f	f	\N	\N	\N	stretch	carry	stretch
512	Mountain Climber	hip_flexors	full body	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	crossfit	rotation	rotation
286	Spell Caster	core	full body	f	f	f	reps	none	f	t	f	f	f	f	f	\N	\N	\N	resistance training	carry	carry
687	Posterior Tibialis Stretch	calves	posterior lower	f	f	f	time	none	f	f	f	f	f	f	f	\N	\N	\N	stretch	carry	stretch
278	Single Leg Butt Kick	glutes	anterior lower	f	f	t	reps	none	t	f	f	f	f	f	t	\N	\N	\N	resistance training	hinge	hinge
322	Yoke Walk	quadriceps	anterior lower	f	f	f	reps	none	f	f	f	f	f	f	t	\N	\N	\N	resistance training	lunge	lunge
327	Body-Up	triceps	posterior upper	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
689	Round The World Shoulder Stretch	side_delts	shoulder	f	f	f	time	none	f	f	f	f	f	f	f	\N	\N	\N	stretch	vertical_push	stretch
368	Underhand Cable Pulldowns	lats	posterior upper	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	resistance training	vertical_pull	vertical_pull
300	Supine Chest Throw	triceps	posterior upper	f	f	f	time	none	f	f	f	f	f	f	t	\N	\N	\N	resistance training	horizontal_push	horizontal_push
323	3/4 Sit-Up	core	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	carry	carry
690	Seated Calf Stretch	calves	posterior lower	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	carry	stretch
511	Incline Dumbbell Press	chest	anterior upper	t	f	f	reps	low	f	t	f	f	f	f	f	\N	\N	13	resistance training	horizontal_push	horizontal_push
500	Squat Cleans	glutes	lower body	t	t	f	reps	none	f	f	t	t	f	f	f	\N	\N	376	resistance training	hinge	hinge
694	Shoulder Circles	side_delts	shoulder	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	mobility	mobility
374	Lateral Burpees Over The Rower	lats	upper body	t	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_pull	burpee
697	Side Lying Floor Stretch	lats	posterior upper	t	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	horizontal_pull	stretch
693	Seated Overhead Stretch	core	core	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	carry	stretch
280	Skating	quadriceps	anterior lower	f	f	f	time	none	f	f	f	f	f	f	f	\N	\N	\N	cardio	squat	squat
501	Strict Handstand Push Ups	front_delts	upper body	t	t	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	vertical_push	vertical_push
494	Overhead Walking Lunges With A Plate	full_body	full body	t	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	crossfit	lunge	lunge
507	Burpee	full_body	full body	f	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	crossfit	carry	burpee
541	Leg Stretch	full_body	lower body	f	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	stretch	carry	stretch
540	Leg Swings (Front And Back)	full_body	lower body	f	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	mobility	hinge	hinge
698	Side Lying Groin Stretch	adductors	posterior lower	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	carry	stretch
382	Deadlift	glutes	posterior lower	t	t	f	reps	moderate	t	f	f	t	f	f	f	\N	\N	7	resistance training	hinge	hinge
552	Back Lever Hold	lats	posterior upper	t	f	f	time	low	t	f	f	f	f	f	f	\N	\N	\N	athletic	horizontal_pull	isometric
550	Full Planche	front_delts	anterior upper	t	t	f	time	low	f	f	f	f	f	f	f	\N	\N	\N	athletic	vertical_push	isometric
8	Romanian Deadlift	hamstrings	posterior lower	t	f	f	reps	moderate	f	t	f	t	f	f	f	\N	\N	9	resistance training	hinge	hinge
551	Planche Push-Up	front_delts	anterior upper	t	t	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
542	Overhead Stretch	front_delts	shoulder	f	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	stretch	vertical_push	stretch
553	Hip Cars	core	core	t	f	f	reps	low	f	f	f	f	f	f	f	\N	\N	\N	mobility	mobility	mobility
10	Hip Thrust	glutes	posterior lower	t	f	f	reps	none	t	t	f	t	f	f	f	\N	\N	\N	resistance training	hinge	hinge
2	Front Squat	quadriceps	anterior lower	t	t	f	reps	none	f	f	f	t	f	f	f	3	\N	1	resistance training	squat	squat
696	Shoulder Stretch	side_delts	shoulder	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	vertical_push	stretch
9	Single Leg Romanian Deadlift	hamstrings	posterior lower	t	f	t	reps	moderate	t	t	t	f	f	f	f	\N	\N	8	resistance training	hinge	hinge
624	V Bar Pullup	lats	posterior upper	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
367	Straight Bar Bench Mid Rows	full_body	full body	t	f	f	time	none	f	f	f	t	f	f	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
625	Wide Grip Rear Pull Up	lats	posterior upper	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	vertical_pull	vertical_pull
67	Machine Crunch	core	full body	f	f	f	time	none	f	f	f	f	t	f	f	\N	\N	103	resistance training	core	core
222	One-Arm Kettlebell Swings	hamstrings	posterior lower	f	f	f	reps	none	f	f	t	f	f	f	f	\N	\N	\N	resistance training	hinge	hinge
85	Barbell Glute Bridge	glutes	posterior lower	f	f	f	reps	none	f	f	f	t	f	f	f	\N	\N	\N	resistance training	hinge	hinge
627	Clean Deadlift	hamstrings	posterior lower	t	t	f	reps	high	f	f	f	t	f	f	f	\N	\N	651	olympic	hinge	hinge
79	Atlas Stones	lower_back	posterior lower	f	f	f	reps	none	f	f	f	f	f	f	t	\N	\N	\N	resistance training	hinge	hinge
84	Skullcrusher	triceps	posterior upper	f	f	f	reps	none	t	t	f	t	f	t	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
86	Shrug	upper_back	posterior upper	f	f	f	reps	none	f	t	f	t	t	f	f	\N	147	\N	resistance training	horizontal_pull	horizontal_pull
386	Foot Handstand Walk	chest	upper body	t	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	resistance training	vertical_push	vertical_push
707	Torso Rotation	core	core	t	f	f	time	none	f	f	f	f	f	f	f	\N	\N	\N	mobility	rotation	rotation
70	Advanced Kettlebell Windmill	core	full body	f	f	f	reps	none	f	f	t	f	f	f	f	\N	\N	\N	resistance training	carry	carry
80	Back Flyes-With Bands	full_body	full body	f	f	f	reps	none	f	f	f	f	f	t	f	\N	\N	\N	resistance training	carry	carry
81	Backward Drag	quadriceps	anterior lower	t	f	f	reps	none	f	f	f	f	f	f	t	\N	\N	\N	resistance training	lunge	sled_drag
628	Clean Pull	quadriceps	anterior lower	t	t	f	reps	high	f	f	f	t	f	f	f	\N	\N	\N	olympic	hinge	vertical_pull
629	Clean Shrug	upper_back	posterior upper	f	t	f	reps	high	f	f	f	t	f	f	f	\N	\N	\N	olympic	horizontal_pull	horizontal_pull
96	Bosu Ball Cable Crunch With Side Bends	core	full body	f	f	f	time	none	f	f	f	f	f	f	f	\N	\N	\N	resistance training	core	core
232	Plate Pinch	forearms	anterior upper	f	f	f	reps	none	f	f	f	f	f	f	t	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
90	Bent-Arm Barbell Pullover	lats	posterior upper	f	f	f	reps	none	f	f	f	t	f	f	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
88	Battling Ropes	full_body	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	carry	carry
97	Bottoms-Up Clean From The Hang Position	glutes	anterior upper	t	t	f	reps	none	f	f	t	f	f	f	f	\N	\N	\N	olympic	hinge	hinge
99	Bradford/Rocky Presses	full_body	full body	t	f	f	reps	none	f	f	f	t	f	f	f	\N	\N	241	resistance training	carry	carry
94	Bicycling, Stationary	quadriceps	anterior lower	f	f	f	time	none	f	f	f	f	t	f	f	\N	\N	\N	cardio	squat	squat
127	Conan'S Wheel	quadriceps	anterior lower	f	f	f	reps	none	f	f	f	f	f	f	t	\N	\N	\N	resistance training	lunge	lunge
102	Cable Crossover	chest	anterior upper	f	f	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
106	Cable Iron Cross	chest	anterior upper	f	f	f	reps	none	f	f	f	f	t	f	f	175	\N	\N	resistance training	horizontal_push	horizontal_push
105	Cable Incline Pushdown	lats	posterior upper	f	f	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
107	Cable Judo Flip	core	full body	f	f	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	carry	carry
116	Calves-Smr	calves	posterior lower	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	stretch	carry	smr
111	Cable Russian Twists	core	full body	f	f	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	rotation	rotation
108	Cable Rear Delt Fly	full_body	full body	f	f	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	carry	carry
388	Jumping Squats	quadriceps	lower body	t	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	376	athletic	squat	plyometric
330	Chair Leg Extended Stretch	hamstrings	posterior lower	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	stretch	hinge	stretch
53	Leg Extension	quadriceps	anterior lower	f	f	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	squat	squat
294	Standing Toe Touches	hamstrings	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	hinge	hinge
121	Chest Push From 3 Point Stance	chest	anterior upper	f	f	f	reps	none	f	f	f	f	f	f	t	\N	\N	\N	resistance training	horizontal_push	horizontal_push
113	Cable Shrugs	upper_back	posterior upper	f	f	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
558	Shoulder Pails/Rails	front_delts	anterior upper	t	f	f	time	low	f	f	f	f	f	f	f	\N	\N	\N	mobility	vertical_push	vertical_push
128	Cross-Body Crunch	core	full body	t	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	core	core
112	Cable Seated Crunch	core	full body	f	f	f	time	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	core	core
117	Car Drivers	full_body	full body	f	f	f	reps	none	f	f	f	t	f	f	f	\N	\N	\N	resistance training	carry	carry
124	Circus Bell	full_body	full body	f	f	f	reps	none	f	t	f	f	f	f	f	\N	\N	\N	resistance training	carry	carry
131	Crunch	core	core	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	core	core
135	Decline Dumbbell Flyes	chest	anterior upper	f	f	f	reps	none	f	t	f	f	t	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
37	Plank	core	anterior upper	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	38	resistance training	carry	isometric
125	Close-Grip Ez-Bar Press	triceps	posterior upper	f	f	f	reps	none	f	f	f	t	f	f	f	\N	\N	337	resistance training	horizontal_push	horizontal_push
369	Upper Back-Leg Grab	hamstrings	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	hinge	hinge
138	Machine Dips	triceps	posterior upper	f	f	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
144	Dumbbell Lying Pronation	forearms	anterior upper	f	f	f	reps	none	f	t	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
145	Dumbbell Lying Supination	forearms	anterior upper	f	f	f	reps	none	f	t	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
141	Double Kettlebell Windmill	full_body	full body	t	t	t	reps	none	f	f	t	f	f	f	f	\N	\N	\N	resistance training	rotation	turkish_get_up
319	Wrist Circles	forearms	anterior upper	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	mobility	mobility
146	Dumbbell Scaption	full_body	full body	f	f	f	reps	none	f	t	f	f	f	f	f	\N	\N	\N	resistance training	carry	carry
98	Brachialis-Smr	biceps	anterior upper	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	mobility	horizontal_pull	smr
150	Elbow Circles	full_body	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	mobility	mobility
642	Olympic Squat	quadriceps	anterior lower	t	t	f	reps	high	f	f	f	t	f	f	f	\N	\N	632	olympic	squat	squat
641	Muscle Snatch	hamstrings	posterior lower	t	t	f	reps	high	f	f	f	t	f	f	f	\N	\N	\N	olympic	hinge	hinge
155	Finger Curls	forearms	anterior upper	f	f	f	reps	none	f	f	f	t	f	f	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
159	Gironda Sternum Chins	lats	posterior upper	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
50	Face Pull	rear_delts	posterior upper	f	f	f	reps	none	f	f	f	f	f	t	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
640	Kneeling Jump Squat	glutes	posterior lower	t	t	f	reps	high	f	f	f	t	f	f	f	\N	\N	\N	olympic	squat	plyometric
158	Frog Hops	quadriceps	anterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	athletic	squat	plyometric
349	On Your Side Quad Stretch	quadriceps	anterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	squat	stretch
153	Extended Range One-Arm Kettlebell Floor Press	chest	anterior upper	f	f	f	reps	none	f	f	t	f	f	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
391	Single-Leg Squats	quadriceps	lower body	t	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	376	resistance training	squat	squat
52	Leg Curl	hamstrings	posterior lower	f	f	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	hinge	hinge
164	Hip Flexion With Band	glutes	anterior lower	f	f	f	reps	none	f	f	f	f	f	t	f	\N	\N	\N	mobility	hinge	hinge
168	Hyperextensions (Back Extensions)	lower_back	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	hinge	hinge
682	One Arm Against Wall	lats	posterior upper	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	horizontal_pull	horizontal_pull
223	One-Arm Side Laterals	full_body	full body	f	f	f	reps	none	f	t	f	f	f	f	f	\N	\N	\N	resistance training	carry	carry
167	Hurdle Hops	hamstrings	posterior lower	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	resistance training	hinge	plyometric
390	Handstand Hold	chest	upper body	t	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	resistance training	vertical_push	isometric
172	Incline Cable Flye	chest	anterior upper	f	f	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
181	Keg Load	lower_back	posterior lower	f	f	f	reps	none	f	f	f	f	f	f	t	\N	\N	\N	resistance training	hinge	hinge
182	Kettlebell Figure 8	full_body	full body	t	t	t	reps	none	f	f	t	f	f	f	f	\N	\N	\N	resistance training	rotation	turkish_get_up
173	Incline Dumbbell Flyes	chest	anterior upper	f	f	f	reps	none	f	t	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
394	Toes-To-Bars	full_body	full body	t	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	crossfit	carry	carry
178	Isometric Neck Exercise-Sides	full_body	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	carry	isometric
526	Hamstring Stretch	hamstrings	posterior lower	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	stretch	hinge	stretch
662	Behind Head Chest Stretch	chest	anterior upper	f	f	f	time	none	f	f	f	f	f	f	f	\N	\N	\N	stretch	horizontal_push	stretch
184	Kettlebell Pirate Ships	full_body	full body	f	f	f	reps	none	f	f	t	f	f	f	f	\N	\N	\N	resistance training	carry	carry
395	Wall Walk	full_body	full body	t	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	crossfit	carry	carry
193	Landmine Linear Jammer	full_body	full body	f	f	f	reps	none	f	f	f	t	f	f	f	\N	\N	\N	resistance training	carry	carry
186	Kettlebell Windmill	full_body	lower body	t	t	t	reps	none	t	f	t	f	f	f	f	\N	\N	\N	resistance training	rotation	turkish_get_up
191	Kneeling Cable Crunch With Alternating Oblique Twists	core	full body	f	f	f	time	none	f	f	f	f	f	f	f	\N	\N	\N	resistance training	core	core
189	Knee/Hip Raise On Parallel Bars	core	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	carry	carry
190	Kneeling Arm Drill	full_body	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	carry	carry
195	Leverage Shrug	upper_back	posterior upper	f	f	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
361	Side Leg Raises	abductors	lower body	f	f	t	reps	none	t	f	f	f	t	t	f	\N	\N	\N	mobility	carry	activation
194	Latissimus Dorsi-Smr	lats	posterior upper	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	mobility	horizontal_pull	smr
224	One-Legged Cable Kickback	glutes	posterior lower	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	resistance training	hinge	hinge
197	Linear Acceleration Wall Drill	hamstrings	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	crossfit	hinge	hinge
170	Iliotibial Tract-Smr	adductors	lower body	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	mobility	carry	smr
176	Iron Crosses (Stretch)	quadriceps	anterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	squat	stretch
201	Low Cable Crossover	chest	anterior upper	f	f	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
58	Wall Slide	upper_back	posterior upper	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	horizontal_pull	horizontal_pull
203	Lying Close-Grip Barbell Triceps Press To Chin	triceps	posterior upper	f	f	f	reps	none	f	f	f	t	f	f	f	\N	\N	125	resistance training	horizontal_push	horizontal_push
73	Ankle Circles	calves	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	mobility	mobility
596	Lateral Bound	adductors	posterior lower	f	f	t	reps	low	t	f	f	f	f	f	f	\N	\N	\N	athletic	carry	plyometric
603	Plyo Push Up	chest	anterior upper	t	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
401	Box Step-Ups	full_body	full body	t	f	f	reps	none	f	t	f	f	f	f	f	\N	\N	\N	resistance training	lunge	lunge
210	Machine Preacher Curls	biceps	anterior upper	f	f	f	reps	none	f	f	f	f	t	f	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
556	Ankle Cars	calves	anterior lower	f	f	f	reps	low	t	f	f	f	f	f	f	\N	\N	\N	mobility	mobility	mobility
488	Handstand Walk	front_delts	upper body	t	t	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	vertical_push	vertical_push
244	Pyramid	lower_back	posterior lower	f	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	mobility	hinge	hinge
316	Wide Stance Stiff Legs	hamstrings	posterior lower	f	f	f	reps	none	f	f	f	t	f	f	f	\N	\N	\N	mobility	hinge	hinge
454	Russian Kettlebell Swings	full_body	full body	t	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	crossfit	hinge	hinge
325	Alternate Leg Diagonal Bound	quadriceps	anterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	squat	plyometric
383	Double-Unders	full_body	full body	t	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	athletic	carry	plyometric
331	Chair Lower Back Stretch	lats	posterior upper	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	horizontal_pull	stretch
320	Wrist Roller	forearms	anterior upper	f	f	f	reps	none	f	t	f	t	t	f	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
404	Hand Release Push Ups	full_body	full body	t	f	f	reps	none	f	f	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_push	horizontal_push
310	Tuck Crunch	core	full body	f	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	core	core
75	Anterior Tibialis-Smr	calves	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	stretch	carry	smr
299	Superman	lower_back	posterior lower	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	rotation	rotation
309	Toe Touchers	core	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	mobility	carry	carry
555	Thoracic Spine Cars	upper_back	posterior upper	f	f	f	reps	low	f	f	f	f	f	f	f	\N	\N	\N	mobility	mobility	mobility
317	Wind Sprints	core	full body	f	f	f	reps	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	carry	carry
393	Thruster	quadriceps	lower body	t	f	f	reps	none	t	t	t	f	f	f	t	\N	\N	\N	resistance training	squat	squat
554	Shoulder Cars	upper_back	shoulder	f	f	f	reps	low	f	f	f	f	f	f	f	\N	\N	\N	mobility	mobility	mobility
645	Power Jerk	quadriceps	anterior lower	t	t	f	reps	high	f	f	f	t	f	f	f	\N	\N	\N	olympic	squat	squat
639	Jerk Dip Squat	quadriceps	anterior lower	t	t	f	reps	high	f	f	f	t	f	f	f	\N	\N	632	olympic	squat	squat
644	Power Clean From Blocks	hamstrings	posterior lower	t	t	f	reps	high	f	f	f	t	f	f	f	\N	\N	\N	olympic	hinge	hinge
646	Power Snatch	hamstrings	posterior lower	t	t	f	reps	high	f	f	f	t	f	f	f	\N	\N	\N	olympic	hinge	hinge
667	Crossover Reverse Lunge	lower_back	posterior lower	t	f	f	time	none	t	f	f	f	f	f	f	\N	\N	\N	resistance training	horizontal_pull	horizontal_pull
643	Overhead Squat	quadriceps	anterior lower	t	t	f	reps	high	f	t	t	t	f	f	f	\N	\N	632	resistance training	squat	squat
\.


--
-- Data for Name: movements_backup_20260228; Type: TABLE DATA; Schema: public; Owner: jacked
--

COPY public.movements_backup_20260228 (id, name, primary_region, bodyweight_possible, dumbbell_possible, kettlebell_possible, barbell_possible, machine_possible, band_possible, plate_or_med_ball_possible, pattern, pattern_subtype, backup_timestamp) FROM stdin;
637	Heaving Snatch Balance	anterior lower	f	f	f	t	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
578	Double Leg Butt Kick	anterior lower	t	f	f	f	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
631	Clean From Blocks	anterior lower	f	f	f	t	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
700	Sit Squats	anterior lower	t	f	f	f	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
632	Frankenstein Squat	anterior lower	f	f	f	t	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
600	Natural Glute Ham Raise	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
636	Hang Snatch Below Knees	posterior lower	f	f	f	t	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
654	Snatch Deadlift	posterior lower	f	f	f	t	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
587	Hyperextensions With No Hyperextension Bench	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
633	Hang Clean	anterior lower	f	f	f	t	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
171	Inchworm	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
66	90/90 Hamstring	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
160	Glute Kickback	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
231	Piriformis-Smr	posterior lower	f	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
659	Split Snatch	posterior lower	f	f	f	t	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
672	Hamstring Smr	posterior lower	f	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
657	Split Clean	anterior lower	f	t	t	t	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
658	Split Jerk	anterior lower	f	f	f	t	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
123	Child'S Pose	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
329	Box Skip	posterior lower	f	f	f	f	f	f	f	lunge	lunge	2026-02-28 12:19:15.622915+00
101	Butt Lift (Bridge)	posterior lower	t	f	f	f	f	f	f	lunge	lunge	2026-02-28 12:19:15.622915+00
623	Step Up	posterior lower	t	t	f	t	f	f	f	lunge	lunge	2026-02-28 12:19:15.622915+00
333	Dumbbell Lunges	anterior lower	f	t	f	f	f	f	f	lunge	lunge	2026-02-28 12:19:15.622915+00
346	Lunge Pass Through	posterior lower	f	f	t	f	f	f	f	lunge	lunge	2026-02-28 12:19:15.622915+00
230	Pin Presses	posterior upper	f	f	f	t	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
337	Floor Press With Chains	posterior upper	f	f	f	t	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
602	Overhead Triceps	anterior upper	t	f	f	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
338	Heavy Bag Thrust	anterior upper	t	f	f	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
48	Tricep Extension	posterior upper	f	t	f	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
502	Strict Ring Dips	anterior upper	f	f	f	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
238	Push-Ups-Close Triceps Position	posterior upper	t	f	f	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
621	Standing Towel Triceps Extension	anterior upper	t	f	f	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
411	Ring Push Ups	full body	f	f	f	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
655	Snatch Shrug	posterior upper	f	f	f	t	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
510	Hammer Curl	anterior upper	f	t	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
340	Kettlebell Sumo High Pull	posterior upper	f	f	t	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
359	Seated Two-Arm Palms-Up Low-Pulley Wrist Curl	anterior upper	f	f	f	f	t	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
47	Bicep Curl	anterior upper	f	t	f	t	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
251	Reverse Barbell Preacher Curls	anterior upper	f	f	f	t	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
581	Freehand Jump Squat	anterior lower	t	f	f	f	f	f	f	squat	plyometric	2026-02-28 12:19:15.622915+00
564	Bench Jump	anterior lower	t	f	f	f	f	f	f	squat	plyometric	2026-02-28 12:19:15.622915+00
611	Rocket Jump	anterior lower	t	f	f	f	f	f	f	squat	plyometric	2026-02-28 12:19:15.622915+00
612	Scissors Jump	anterior lower	t	f	f	f	f	f	f	squat	plyometric	2026-02-28 12:19:15.622915+00
534	Jumping Lunge	anterior lower	t	f	f	f	f	f	f	lunge	plyometric	2026-02-28 12:19:15.622915+00
593	Isometric Chest Squeezes	anterior upper	t	f	f	f	f	f	f	horizontal_push	isometric	2026-02-28 12:19:15.622915+00
179	Isometric Wipers	anterior upper	t	f	f	f	f	f	f	horizontal_push	isometric	2026-02-28 12:19:15.622915+00
528	Quad Stretch	anterior lower	t	f	f	f	f	f	f	squat	stretch	2026-02-28 12:19:15.622915+00
691	Seated Floor Hamstring Stretch	posterior lower	t	f	f	f	f	f	f	hinge	stretch	2026-02-28 12:19:15.622915+00
692	Seated Hamstring And Calf Stretch	posterior lower	f	f	f	f	f	f	f	hinge	stretch	2026-02-28 12:19:15.622915+00
668	Dancer'S Stretch	posterior lower	t	f	f	f	f	f	f	hinge	stretch	2026-02-28 12:19:15.622915+00
356	Runner'S Stretch	posterior lower	t	f	f	f	f	f	f	hinge	stretch	2026-02-28 12:19:15.622915+00
371	World'S Greatest Stretch	posterior lower	t	f	f	f	f	f	f	hinge	stretch	2026-02-28 12:19:15.622915+00
339	Intermediate Groin Stretch	posterior lower	f	f	f	f	f	f	f	hinge	stretch	2026-02-28 12:19:15.622915+00
703	Standing Hamstring And Calf Stretch	posterior lower	f	f	f	f	f	f	f	hinge	stretch	2026-02-28 12:19:15.622915+00
543	Doorway Stretch	upper body	t	f	f	f	f	f	f	horizontal_push	stretch	2026-02-28 12:19:15.622915+00
708	Tricep Side Stretch	anterior upper	t	f	f	f	f	f	f	horizontal_push	stretch	2026-02-28 12:19:15.622915+00
709	Triceps Stretch	anterior upper	t	f	f	f	f	f	f	horizontal_push	stretch	2026-02-28 12:19:15.622915+00
634	Hang Clean Below The Knees	anterior lower	f	f	f	t	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
245	Quadriceps-Smr	anterior lower	f	f	f	f	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
688	Quadriceps Smr	anterior lower	f	f	f	f	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
256	Reverse Hyperextension	posterior lower	f	f	f	f	t	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
635	Hang Snatch	posterior lower	f	f	f	t	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
312	Weighted Ball Hyperextension	posterior lower	f	f	f	f	f	f	t	hinge	hinge	2026-02-28 12:19:15.622915+00
228	Pelvic Tilt Into Bridge	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
293	Standing Pelvic Tilt	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
56	Cat-Cow	posterior upper	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
248	Rack Pulls	posterior lower	f	f	f	t	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
227	One Knee To Chest	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
298	Straight-Arm Dumbbell Pullover	anterior upper	f	t	f	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
363	Speed Band Overhead Triceps	posterior upper	f	f	f	f	f	t	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
243	Pushups (Close And Wide Hand Positions)	anterior upper	t	f	f	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
663	Brachialis Smr	anterior upper	f	f	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
273	Seated One-Arm Cable Pulley Rows	posterior upper	f	f	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
255	Reverse Grip Bent-Over Rows	full body	f	f	f	t	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
24	Seated Cable Row	posterior upper	f	f	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
25	Inverted Row	posterior upper	t	f	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
588	Incline Push Up	anterior upper	t	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
589	Incline Push Up Close Grip	anterior upper	t	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
590	Incline Push Up Medium	anterior upper	t	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
591	Incline Push Up Reverse Grip	anterior upper	t	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
592	Incline Push Up Wide	anterior upper	t	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
572	Close Grip Push Up Off Of A Dumbbell	anterior upper	t	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
585	Hanging Pike	core	t	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
605	Push Up Wide	anterior upper	t	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
606	Push Ups Close Triceps Position	anterior upper	t	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
577	Dips Triceps Version	anterior upper	t	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
616	Single Arm Push Up	anterior upper	t	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
638	Jerk Balance	shoulder	f	f	f	t	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
648	Push Press	shoulder	f	f	f	t	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
607	Push Ups With Feet Elevated	anterior upper	t	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
49	Lateral Raise	shoulder	f	t	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
16	Push-Up	anterior upper	t	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
649	Push Press Behind The Neck	shoulder	f	f	f	t	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
608	Push Up To Side Plank	anterior upper	t	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
563	Bench Dips	anterior upper	t	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
571	Clock Push Up	anterior upper	t	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
302	Supine Two-Arm Overhead Throw	shoulder	f	f	f	f	f	f	t	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
295	Standing Two-Arm Overhead Throw	shoulder	f	f	f	f	f	f	t	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
594	Jackknife Sit Up	core	t	f	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
565	Bent Knee Hip Raise	core	t	f	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
569	Butt Ups	core	t	f	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
573	Cocoons	core	t	f	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
407	Knees To Elbows	core	f	f	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
314	Weighted Sit-Ups-With Bands	full body	f	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
192	Landmine 180'S	full body	f	f	f	t	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
328	Bottoms Up	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
350	Otis-Up	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
345	Lower Back Curl	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
360	Side Jackknife	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
617	Sit Up	core	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
72	Alternate Heel Touchers	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
188	Knee Circles	posterior lower	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
246	Quick Leap	anterior lower	f	f	f	f	f	f	f	squat	plyometric	2026-02-28 12:19:15.622915+00
122	Chest Stretch On Stability Ball	anterior upper	f	f	f	f	f	f	f	horizontal_push	stretch	2026-02-28 12:19:15.622915+00
120	Chest And Front Of Shoulder Stretch	anterior upper	f	f	f	f	f	f	f	horizontal_push	stretch	2026-02-28 12:19:15.622915+00
527	Lat Stretch	posterior upper	t	f	f	f	f	f	f	horizontal_pull	stretch	2026-02-28 12:19:15.622915+00
365	Standing Elevated Quad Stretch	anterior lower	f	f	f	f	f	f	f	squat	stretch	2026-02-28 12:19:15.622915+00
324	All Fours Quad Stretch	anterior lower	t	f	f	f	f	f	f	squat	stretch	2026-02-28 12:19:15.622915+00
701	Standing Biceps Stretch	anterior upper	f	f	f	f	f	f	f	horizontal_pull	stretch	2026-02-28 12:19:15.622915+00
711	Upward Stretch	shoulder	t	f	f	f	f	f	f	vertical_push	stretch	2026-02-28 12:19:15.622915+00
669	Dynamic Chest Stretch	anterior upper	t	f	f	f	f	f	f	horizontal_push	dynamic_warmup	2026-02-28 12:19:15.622915+00
277	Single-Cone Sprint Drill	anterior lower	f	f	f	f	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
647	Power Snatch From Blocks	anterior lower	f	f	f	t	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
656	Snatch From Blocks	anterior lower	f	f	f	t	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
491	Kettlebell Goblet Squats	lower body	f	f	f	f	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
364	Split Squats	posterior lower	t	f	f	f	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
1	Back Squat	anterior lower	f	f	f	t	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
3	Goblet Squat	anterior lower	f	t	t	f	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
376	Air Squat	lower body	f	f	f	f	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
61	Wall Sit	anterior lower	t	f	f	f	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
12	Kettlebell Swing	posterior lower	f	f	t	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
509	Deficit Deadlift	posterior lower	f	f	f	t	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
7	Conventional Deadlift	posterior lower	f	f	f	t	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
651	Romanian Deadlift From Deficit	posterior lower	f	f	f	t	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
679	Lower Back Smr	posterior lower	f	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
204	Lying Crossover	lower body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
215	Neck-Smr	full body	f	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
259	Rhomboids-Smr	full body	f	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
586	Hip Circles (Prone)	posterior lower	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
212	Monster Walk	lower body	f	f	f	f	f	t	f	carry	carry	2026-02-28 12:19:15.622915+00
247	Rack Delivery	full body	f	f	f	t	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
253	Reverse Flyes	full body	f	t	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
254	Reverse Flyes With External Rotation	full body	f	t	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
257	Reverse Machine Flyes	full body	f	f	f	f	t	f	f	carry	carry	2026-02-28 12:19:15.622915+00
250	Return Push From Stance	full body	f	f	f	f	f	f	t	carry	carry	2026-02-28 12:19:15.622915+00
68	Adductor	lower body	f	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
162	Groiners	lower body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
304	Suspended Reverse Crunch	full body	f	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
313	Weighted Crunches	full body	f	f	f	f	f	f	t	carry	carry	2026-02-28 12:19:15.622915+00
39	Dead Bug	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
134	Decline Crunch	core	f	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
136	Decline Oblique Crunch	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
137	Decline Reverse Crunch	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
161	Gorilla Chin/Crunch	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
216	Oblique Crunches	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
521	Cardio Intervals	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
684	Peroneals Smr	posterior lower	f	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
665	Calves Smr	posterior lower	f	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
266	Sandbag Load	anterior lower	f	f	f	f	f	f	t	carry	carry	2026-02-28 12:19:15.622915+00
115	Calf Stretch Hands Against Wall	posterior lower	t	f	f	f	f	f	f	carry	stretch	2026-02-28 12:19:15.622915+00
522	Foam Rolling	full body	f	f	f	f	f	f	f	carry	foam_roll	2026-02-28 12:19:15.622915+00
402	Chest To Bar Pull Ups	full body	f	f	f	f	f	f	f	vertical_pull	vertical_pull	2026-02-28 12:19:15.622915+00
515	Upright Row	shoulder	f	f	f	t	f	f	f	vertical_pull	vertical_pull	2026-02-28 12:19:15.622915+00
28	Lat Pulldown	posterior upper	f	f	f	f	f	f	f	vertical_pull	vertical_pull	2026-02-28 12:19:15.622915+00
676	Kneeling Hip Flexor	anterior lower	t	f	f	f	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
680	Lying Hamstring	posterior lower	f	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
686	Piriformis Smr	posterior lower	f	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
683	Overhead Lat	posterior upper	f	f	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
677	Latissimus Dorsi Smr	posterior upper	f	f	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
699	Side Wrist Pull	shoulder	t	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
674	Iliotibial Tract Smr	posterior lower	f	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
678	Leg Up Hamstring Stretch	posterior lower	t	f	f	f	f	f	f	hinge	stretch	2026-02-28 12:19:15.622915+00
533	Jumping Jacks	full body	t	f	f	f	f	f	f	carry	plyometric	2026-02-28 12:19:15.622915+00
400	Rowing Machine	full body	f	f	f	f	t	f	f	carry	row	2026-02-28 12:19:15.622915+00
671	Groin And Back Stretch	posterior lower	t	f	f	f	f	f	f	carry	stretch	2026-02-28 12:19:15.622915+00
583	Front Leg Raises	core	t	f	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
615	Side Bridge	core	t	f	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
610	Rear Leg Raises	anterior lower	t	f	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
613	Seated Flat Bench Leg Pull In	core	t	f	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
268	Seated Barbell Twist	full body	f	f	f	t	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
174	Incline Dumbbell Flyes-With A Twist	anterior upper	f	t	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
265	Russian Twist	full body	t	f	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
64	Battle Rope Wave	full body	f	f	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
598	Leg Pull In	core	t	f	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
670	Foot Smr	posterior lower	f	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
31	Power Clean	full body	f	f	f	t	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
32	Snatch	full body	f	f	f	t	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
151	Elbow To Knee	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
41	Hanging Leg Raise	core	f	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
42	Ab Wheel Rollout	anterior upper	f	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
661	Anterior Tibialis Smr	posterior lower	f	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
287	Spider Crawl	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
306	Thigh Abductor	lower body	f	f	f	f	t	f	f	carry	carry	2026-02-28 12:19:15.622915+00
307	Thigh Adductor	lower body	f	f	f	f	t	f	f	carry	carry	2026-02-28 12:19:15.622915+00
595	Janda Sit Up	core	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
279	Single Leg Glute Bridge	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
11	Good Morning	posterior lower	f	f	f	t	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
275	Single-Arm Cable Crossover	anterior upper	f	f	f	f	t	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
14	Incline Bench Press	anterior upper	f	t	f	t	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
23	Single Arm Row	posterior upper	f	t	t	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
276	Single-Arm Linear Jammer	full body	f	f	f	t	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
55	Pigeon Stretch	posterior lower	t	f	f	f	f	f	f	hinge	stretch	2026-02-28 12:19:15.622915+00
568	Squat	anterior lower	t	f	f	f	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
285	Smith Machine One-Arm Upright Row	full body	f	f	f	f	t	f	f	carry	carry	2026-02-28 12:19:15.622915+00
618	Split Jump	anterior lower	t	f	f	f	f	f	f	squat	plyometric	2026-02-28 12:19:15.622915+00
620	Standing Long Jump	anterior lower	t	f	f	f	f	f	f	squat	plyometric	2026-02-28 12:19:15.622915+00
622	Star Jump	anterior lower	t	f	f	f	f	f	f	squat	plyometric	2026-02-28 12:19:15.622915+00
666	Cat Stretch	posterior lower	t	f	f	f	f	f	f	hinge	stretch	2026-02-28 12:19:15.622915+00
214	Moving Claw Series	posterior lower	t	f	f	f	f	f	f	lunge	lunge	2026-02-28 12:19:15.622915+00
234	Platform Hamstring Slides	posterior lower	f	f	f	f	f	f	f	lunge	lunge	2026-02-28 12:19:15.622915+00
236	Prone Manual Hamstring	posterior lower	t	f	f	f	f	f	f	lunge	lunge	2026-02-28 12:19:15.622915+00
315	Wide-Grip Decline Barbell Pullover	anterior upper	f	f	f	t	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
258	Reverse Plate Curls	anterior upper	f	f	f	f	f	f	t	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
292	Standing Olympic Plate Hand Squeeze	anterior upper	f	f	f	f	f	f	t	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
284	Smith Machine Behind The Back Shrug	posterior upper	f	f	f	f	t	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
274	Side To Side Chins	posterior upper	f	f	f	f	t	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
233	Plate Twist	full body	f	f	f	f	f	f	t	rotation	rotation	2026-02-28 12:19:15.622915+00
580	Flat Bench Lying Leg Raise	core	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
582	Frog Sit Ups	core	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
211	Mixed Grip Chin	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
283	Sledgehammer Swings	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
303	Suspended Fallout	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
272	Seated Head Harness Neck Resistance	full body	f	f	f	f	f	f	t	carry	carry	2026-02-28 12:19:15.622915+00
282	Sled Reverse Flye	full body	f	f	f	f	t	f	f	carry	carry	2026-02-28 12:19:15.622915+00
290	Standing Cable Lift	full body	f	f	f	f	t	f	f	carry	carry	2026-02-28 12:19:15.622915+00
326	Band Hip Adductions	lower body	f	f	f	f	f	t	f	carry	carry	2026-02-28 12:19:15.622915+00
576	Crunch Legs On Exercise Ball	core	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
291	Standing Cable Wood Chop	full body	f	f	f	f	t	f	f	carry	plyometric	2026-02-28 12:19:15.622915+00
343	Lateral Cone Hops	lower body	t	f	f	f	f	f	f	carry	plyometric	2026-02-28 12:19:15.622915+00
249	Recumbent Bike	anterior lower	f	f	f	f	t	f	f	squat	bike	2026-02-28 12:19:15.622915+00
209	Lying Prone Quadriceps	anterior lower	t	f	f	f	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
200	Looking At Ceiling	anterior lower	t	f	f	f	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
225	One Half Locust	anterior lower	t	f	f	f	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
165	Hug A Ball	posterior lower	f	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
166	Hug Knees To Chest	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
270	Seated Glute	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
74	Ankle On The Knee	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
187	Knee Across The Body	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
335	Elbows Back	anterior upper	t	f	f	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
269	Seated Biceps	anterior upper	t	f	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
226	One Handed Hang	posterior upper	f	f	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
252	Reverse Crunch	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
297	Stomach Vacuum	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
267	Scissor Kick	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
358	Seated Front Deltoid	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
76	Arm Circles	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
202	Lying Bent Leg Groin	lower body	f	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
341	Knee Tuck Jump	posterior lower	t	f	f	f	f	f	f	hinge	plyometric	2026-02-28 12:19:15.622915+00
264	Running, Treadmill	posterior lower	f	f	f	f	t	f	f	hinge	run	2026-02-28 12:19:15.622915+00
389	Run	posterior lower	f	f	f	f	f	f	f	hinge	run	2026-02-28 12:19:15.622915+00
342	Kneeling Forearm Stretch	anterior upper	t	f	f	f	f	f	f	horizontal_pull	stretch	2026-02-28 12:19:15.622915+00
110	Cable Rope Rear-Delt Rows	shoulder	f	f	f	f	t	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
372	Calorie Row	upper body	f	f	f	f	t	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
673	It Band And Glute Stretch	posterior lower	f	f	f	f	f	f	f	carry	stretch	2026-02-28 12:19:15.622915+00
65	Turkish Get-Up	full body	f	t	t	f	f	f	f	carry	turkish_get_up	2026-02-28 12:19:15.622915+00
301	Supine One-Arm Overhead Throw	shoulder	f	f	f	f	f	f	t	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
305	The Straddle	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
695	Shoulder Raise	shoulder	t	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
29	Muscle-Up	posterior upper	t	f	f	f	f	f	f	vertical_pull	vertical_pull	2026-02-28 12:19:15.622915+00
33	Clean and Jerk	posterior lower	f	f	f	t	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
614	Seated Leg Tucks	core	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
579	Flat Bench Leg Pull In	core	t	f	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
332	Chair Upper Body Stretch	full body	f	f	f	f	f	f	f	carry	stretch	2026-02-28 12:19:15.622915+00
347	Middle Back Stretch	full body	t	f	f	f	f	f	f	carry	stretch	2026-02-28 12:19:15.622915+00
62	Sprint	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
142	Downward Facing Balance	posterior lower	f	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
71	Calorie Echo Bike	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
281	Sled Drag-Harness	anterior lower	f	f	f	f	t	f	f	carry	sled_drag	2026-02-28 12:19:15.622915+00
89	Bear Crawl Sled Drags	anterior lower	f	f	f	f	f	f	t	carry	bear_crawl	2026-02-28 12:19:15.622915+00
334	Dynamic Back Stretch	posterior upper	t	f	f	f	f	f	f	horizontal_pull	dynamic_warmup	2026-02-28 12:19:15.622915+00
152	Elliptical Trainer	anterior lower	f	f	f	f	t	f	f	squat	squat	2026-02-28 12:19:15.622915+00
180	Jogging, Treadmill	anterior lower	f	f	f	f	t	f	f	squat	squat	2026-02-28 12:19:15.622915+00
6	Walking Lunge	anterior lower	t	t	f	f	f	f	f	lunge	lunge	2026-02-28 12:19:15.622915+00
235	Plyo Kettlebell Pushups	anterior upper	f	f	t	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
46	Medicine Ball Slam	full body	f	f	f	f	f	f	t	rotation	rotation	2026-02-28 12:19:15.622915+00
45	Depth Jump	anterior lower	f	f	f	f	f	f	f	squat	plyometric	2026-02-28 12:19:15.622915+00
262	Rope Jumping	anterior lower	f	f	f	f	f	f	f	squat	plyometric	2026-02-28 12:19:15.622915+00
44	Broad Jump	posterior lower	t	f	f	f	f	f	f	hinge	plyometric	2026-02-28 12:19:15.622915+00
289	Stairmaster	anterior lower	f	f	f	f	t	f	f	squat	squat	2026-02-28 12:19:15.622915+00
296	Step Mill	anterior lower	f	f	f	f	t	f	f	lunge	lunge	2026-02-28 12:19:15.622915+00
377	Back-Rack Barbell Carry	full body	f	f	f	t	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
523	Mobility For Lower Back	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
57	Thoracic Rotation	posterior upper	t	f	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
381	Candlestick Rocks	full body	f	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
531	High Rep Push-Up	anterior upper	t	f	f	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
535	Pause Squat	anterior lower	f	f	f	t	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
536	Reverse Fly	shoulder	f	t	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
529	Leg Swings	anterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
546	Snatch Balance	anterior lower	f	f	f	t	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
547	Tall Clean	anterior lower	f	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
544	One-Arm Kettlebell Military Press To The Side	shoulder	f	f	t	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
537	Seated Leg Raise	full body	t	f	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
40	Pallof Press	anterior upper	f	f	f	f	f	t	f	rotation	rotation	2026-02-28 12:19:15.622915+00
348	On-Your-Back Quad Stretch	anterior lower	f	f	f	f	f	f	f	squat	stretch	2026-02-28 12:19:15.622915+00
525	Chest Stretch	anterior upper	t	f	f	f	f	f	f	horizontal_push	stretch	2026-02-28 12:19:15.622915+00
524	Calf Stretch	posterior lower	t	f	f	f	f	f	f	carry	stretch	2026-02-28 12:19:15.622915+00
548	Tuck Planche	anterior upper	f	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
549	Straddle Planche	anterior upper	f	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
545	Rest	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
4	Pistol Squat	anterior lower	t	f	f	f	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
559	Hamstring Pails/Rails	posterior lower	f	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
196	Linear 3-Part Start Technique	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
13	Bench Press	anterior upper	f	t	f	t	t	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
560	Thoracic Pails/Rails	posterior upper	f	f	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
22	Barbell Row	posterior upper	f	f	f	t	t	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
18	Overhead Press	shoulder	f	f	f	t	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
26	Pull-Up	posterior upper	t	f	f	f	f	f	f	vertical_pull	vertical_pull	2026-02-28 12:19:15.622915+00
557	Hip Pails/Rails	anterior lower	f	f	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
370	Upper Back Stretch	full body	t	f	f	f	f	f	f	carry	stretch	2026-02-28 12:19:15.622915+00
5	Bulgarian Split Squat	anterior lower	t	t	f	t	f	f	f	lunge	lunge	2026-02-28 12:19:15.622915+00
27	Chin-Up	posterior upper	t	f	f	f	f	f	f	vertical_pull	vertical_pull	2026-02-28 12:19:15.622915+00
30	Clean	full body	f	f	f	t	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
43	Box Jump	anterior lower	f	f	f	f	f	f	f	squat	plyometric	2026-02-28 12:19:15.622915+00
704	Standing Hip Flexors	anterior lower	t	f	f	f	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
104	Cable Deadlifts	anterior lower	f	f	f	f	t	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
17	Dip	anterior upper	t	f	f	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
19	Dumbbell Shoulder Press	shoulder	f	t	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
103	Cable Crunch	full body	f	f	f	f	t	f	f	carry	carry	2026-02-28 12:19:15.622915+00
109	Cable Reverse Crunch	full body	f	f	f	f	t	f	f	carry	carry	2026-02-28 12:19:15.622915+00
379	Burpees	full body	f	f	f	f	f	f	f	carry	burpee	2026-02-28 12:19:15.622915+00
20	Pike Push-Up	shoulder	t	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
38	Side Plank	anterior upper	t	f	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
36	Overhead Carry	full body	f	t	t	t	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
59	L-Sit Hold	anterior upper	t	f	f	f	f	f	f	rotation	isometric	2026-02-28 12:19:15.622915+00
34	Farmer'S Carry	full body	f	t	t	t	f	f	f	carry	farmer_carry	2026-02-28 12:19:15.622915+00
35	Offset Suitcase Carry	full body	f	t	t	f	f	f	f	carry	suitcase_carry	2026-02-28 12:19:15.622915+00
705	Standing Lateral Stretch	core	t	f	f	f	f	f	f	rotation	stretch	2026-02-28 12:19:15.622915+00
706	Standing Soleus And Achilles Stretch	posterior lower	t	f	f	f	f	f	f	carry	stretch	2026-02-28 12:19:15.622915+00
21	Handstand Push-Up	shoulder	t	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
63	Sled Push	anterior lower	f	f	f	f	f	f	t	carry	sled_push	2026-02-28 12:19:15.622915+00
408	Wall Ball	full body	f	f	f	f	f	f	t	squat	squat	2026-02-28 12:19:15.622915+00
93	Bicycling	anterior lower	f	f	f	f	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
95	Bodyweight Flyes	anterior upper	f	f	f	t	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
77	Around The Worlds	anterior upper	f	t	t	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
60	Front Lever Hold	posterior upper	t	f	f	f	f	f	f	horizontal_pull	isometric	2026-02-28 12:19:15.622915+00
308	Tire Flip	anterior lower	f	f	f	f	f	f	t	hinge	hinge	2026-02-28 12:19:15.622915+00
118	Carioca Quick Step	lower body	t	f	f	f	f	f	f	lunge	lunge	2026-02-28 12:19:15.622915+00
143	Dumbbell Flyes	anterior upper	f	t	f	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
119	Catch And Overhead Throw	posterior upper	f	f	f	f	f	f	t	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
412	Sandbag Carry	full body	f	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
130	Crucifix	full body	f	t	t	f	f	f	t	carry	carry	2026-02-28 12:19:15.622915+00
213	Mountain Climbers	anterior lower	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
154	Fast Skipping	anterior lower	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
51	Calf Raise	anterior lower	t	t	f	f	t	f	f	carry	carry	2026-02-28 12:19:15.622915+00
175	Iron Cross	full body	f	t	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
177	Isometric Neck Exercise-Front And Back	full body	t	f	f	f	f	f	f	carry	isometric	2026-02-28 12:19:15.622915+00
156	Flutter Kicks	posterior lower	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
183	Kettlebell Pass Between The Legs	full body	f	f	t	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
199	London Bridges	posterior upper	f	f	f	f	f	f	t	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
398	Ghd Sit Ups	full body	f	f	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
198	Log Lift	full body	f	f	f	f	f	f	t	carry	carry	2026-02-28 12:19:15.622915+00
261	Rope Climb	posterior upper	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
406	Kettlebell Turkish Get Ups	full body	f	f	t	f	f	f	f	carry	turkish_get_up	2026-02-28 12:19:15.622915+00
54	Hip Flexor Stretch	anterior lower	t	f	f	f	f	f	f	carry	stretch	2026-02-28 12:19:15.622915+00
435	Alternating Dumbbell Snatches	posterior lower	f	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
260	Ring Dips	posterior upper	f	f	f	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
239	Push-Ups With Feet Elevated	anterior upper	t	f	f	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
241	Push Press-Behind The Neck	full body	f	f	f	t	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
685	Peroneals Stretch	posterior lower	f	f	f	f	f	f	f	carry	stretch	2026-02-28 12:19:15.622915+00
278	Single Leg Butt Kick	anterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
512	Mountain Climber	full body	t	f	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
286	Spell Caster	full body	f	t	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
687	Posterior Tibialis Stretch	posterior lower	f	f	f	f	f	f	f	carry	stretch	2026-02-28 12:19:15.622915+00
322	Yoke Walk	anterior lower	f	f	f	f	f	f	t	lunge	lunge	2026-02-28 12:19:15.622915+00
327	Body-Up	posterior upper	t	f	f	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
300	Supine Chest Throw	posterior upper	f	f	f	f	f	f	t	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
368	Underhand Cable Pulldowns	posterior upper	f	f	f	f	f	f	f	vertical_pull	vertical_pull	2026-02-28 12:19:15.622915+00
323	3/4 Sit-Up	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
689	Round The World Shoulder Stretch	shoulder	f	f	f	f	f	f	f	vertical_push	stretch	2026-02-28 12:19:15.622915+00
690	Seated Calf Stretch	posterior lower	t	f	f	f	f	f	f	carry	stretch	2026-02-28 12:19:15.622915+00
500	Squat Cleans	lower body	f	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
511	Incline Dumbbell Press	anterior upper	f	t	f	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
694	Shoulder Circles	shoulder	t	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
374	Lateral Burpees Over The Rower	upper body	f	f	f	f	f	f	f	horizontal_pull	burpee	2026-02-28 12:19:15.622915+00
697	Side Lying Floor Stretch	posterior upper	t	f	f	f	f	f	f	horizontal_pull	stretch	2026-02-28 12:19:15.622915+00
693	Seated Overhead Stretch	core	t	f	f	f	f	f	f	carry	stretch	2026-02-28 12:19:15.622915+00
280	Skating	anterior lower	f	f	f	f	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
501	Strict Handstand Push Ups	upper body	f	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
540	Leg Swings (Front And Back)	lower body	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
382	Deadlift	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
494	Overhead Walking Lunges With A Plate	full body	f	f	f	f	f	f	f	lunge	lunge	2026-02-28 12:19:15.622915+00
507	Burpee	full body	t	f	f	f	f	f	f	carry	burpee	2026-02-28 12:19:15.622915+00
541	Leg Stretch	lower body	t	f	f	f	f	f	f	carry	stretch	2026-02-28 12:19:15.622915+00
698	Side Lying Groin Stretch	posterior lower	t	f	f	f	f	f	f	carry	stretch	2026-02-28 12:19:15.622915+00
552	Back Lever Hold	posterior upper	t	f	f	f	f	f	f	horizontal_pull	isometric	2026-02-28 12:19:15.622915+00
550	Full Planche	anterior upper	f	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
2	Front Squat	anterior lower	f	f	f	t	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
8	Romanian Deadlift	posterior lower	f	t	f	t	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
10	Hip Thrust	posterior lower	f	t	f	t	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
551	Planche Push-Up	anterior upper	f	f	f	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
553	Hip Cars	core	f	f	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
357	Seated Flat Bench Leg Pull-In	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
542	Overhead Stretch	shoulder	t	f	f	f	f	f	f	vertical_push	stretch	2026-02-28 12:19:15.622915+00
696	Shoulder Stretch	shoulder	t	f	f	f	f	f	f	vertical_push	stretch	2026-02-28 12:19:15.622915+00
9	Single Leg Romanian Deadlift	posterior lower	t	t	t	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
624	V Bar Pullup	posterior upper	t	f	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
367	Straight Bar Bench Mid Rows	full body	f	f	f	t	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
625	Wide Grip Rear Pull Up	posterior upper	t	f	f	f	f	f	f	vertical_pull	vertical_pull	2026-02-28 12:19:15.622915+00
67	Machine Crunch	full body	f	f	f	f	t	f	f	carry	carry	2026-02-28 12:19:15.622915+00
628	Clean Pull	anterior lower	f	f	f	t	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
222	One-Arm Kettlebell Swings	posterior lower	f	f	t	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
85	Barbell Glute Bridge	posterior lower	f	f	f	t	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
627	Clean Deadlift	posterior lower	f	f	f	t	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
79	Atlas Stones	posterior lower	f	f	f	f	f	f	t	hinge	hinge	2026-02-28 12:19:15.622915+00
81	Backward Drag	anterior lower	f	f	f	f	f	f	t	lunge	lunge	2026-02-28 12:19:15.622915+00
84	Skullcrusher	posterior upper	t	t	f	t	f	t	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
629	Clean Shrug	posterior upper	f	f	f	t	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
86	Shrug	posterior upper	f	t	f	t	t	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
386	Foot Handstand Walk	upper body	f	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
707	Torso Rotation	core	f	f	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
70	Advanced Kettlebell Windmill	full body	f	f	t	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
80	Back Flyes-With Bands	full body	f	f	f	f	f	t	f	carry	carry	2026-02-28 12:19:15.622915+00
97	Bottoms-Up Clean From The Hang Position	anterior upper	f	f	t	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
232	Plate Pinch	anterior upper	f	f	f	f	f	f	t	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
90	Bent-Arm Barbell Pullover	posterior upper	f	f	f	t	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
88	Battling Ropes	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
96	Bosu Ball Cable Crunch With Side Bends	full body	f	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
99	Bradford/Rocky Presses	full body	f	f	f	t	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
94	Bicycling, Stationary	anterior lower	f	f	f	f	t	f	f	squat	squat	2026-02-28 12:19:15.622915+00
127	Conan'S Wheel	anterior lower	f	f	f	f	f	f	t	lunge	lunge	2026-02-28 12:19:15.622915+00
102	Cable Crossover	anterior upper	f	f	f	f	t	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
106	Cable Iron Cross	anterior upper	f	f	f	f	t	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
105	Cable Incline Pushdown	posterior upper	f	f	f	f	t	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
107	Cable Judo Flip	full body	f	f	f	f	t	f	f	carry	carry	2026-02-28 12:19:15.622915+00
111	Cable Russian Twists	full body	f	f	f	f	t	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
108	Cable Rear Delt Fly	full body	f	f	f	f	t	f	f	carry	carry	2026-02-28 12:19:15.622915+00
116	Calves-Smr	posterior lower	f	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
388	Jumping Squats	lower body	f	f	f	f	f	f	f	squat	plyometric	2026-02-28 12:19:15.622915+00
330	Chair Leg Extended Stretch	posterior lower	f	f	f	f	f	f	f	hinge	stretch	2026-02-28 12:19:15.622915+00
53	Leg Extension	anterior lower	f	f	f	f	t	f	f	squat	squat	2026-02-28 12:19:15.622915+00
271	Seated Hamstring	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
294	Standing Toe Touches	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
125	Close-Grip Ez-Bar Press	posterior upper	f	f	f	t	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
121	Chest Push From 3 Point Stance	anterior upper	f	f	f	f	f	f	t	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
135	Decline Dumbbell Flyes	anterior upper	f	t	f	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
113	Cable Shrugs	posterior upper	f	f	f	f	t	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
558	Shoulder Pails/Rails	anterior upper	f	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
128	Cross-Body Crunch	full body	t	f	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
112	Cable Seated Crunch	full body	f	f	f	f	t	f	f	carry	carry	2026-02-28 12:19:15.622915+00
117	Car Drivers	full body	f	f	f	t	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
124	Circus Bell	full body	f	t	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
131	Crunch	core	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
37	Plank	anterior upper	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
369	Upper Back-Leg Grab	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
138	Machine Dips	posterior upper	f	f	f	f	t	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
144	Dumbbell Lying Pronation	anterior upper	f	t	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
145	Dumbbell Lying Supination	anterior upper	f	t	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
319	Wrist Circles	anterior upper	t	f	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
141	Double Kettlebell Windmill	full body	f	f	t	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
146	Dumbbell Scaption	full body	f	t	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
642	Olympic Squat	anterior lower	f	f	f	t	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
641	Muscle Snatch	posterior lower	f	f	f	t	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
710	Upper Back Leg Grab	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
153	Extended Range One-Arm Kettlebell Floor Press	anterior upper	f	f	t	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
98	Brachialis-Smr	anterior upper	f	f	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
155	Finger Curls	anterior upper	f	f	f	t	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
159	Gironda Sternum Chins	posterior upper	t	f	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
50	Face Pull	posterior upper	f	f	f	f	f	t	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
150	Elbow Circles	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
640	Kneeling Jump Squat	posterior lower	f	f	f	t	f	f	f	squat	plyometric	2026-02-28 12:19:15.622915+00
158	Frog Hops	anterior lower	t	f	f	f	f	f	f	squat	plyometric	2026-02-28 12:19:15.622915+00
349	On Your Side Quad Stretch	anterior lower	t	f	f	f	f	f	f	squat	stretch	2026-02-28 12:19:15.622915+00
391	Single-Leg Squats	lower body	f	f	f	f	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
52	Leg Curl	posterior lower	f	f	f	f	t	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
164	Hip Flexion With Band	anterior lower	f	f	f	f	f	t	f	hinge	hinge	2026-02-28 12:19:15.622915+00
168	Hyperextensions (Back Extensions)	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
682	One Arm Against Wall	posterior upper	t	f	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
223	One-Arm Side Laterals	full body	f	t	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
167	Hurdle Hops	posterior lower	f	f	f	f	f	f	f	hinge	plyometric	2026-02-28 12:19:15.622915+00
390	Handstand Hold	upper body	f	f	f	f	f	f	f	vertical_push	isometric	2026-02-28 12:19:15.622915+00
172	Incline Cable Flye	anterior upper	f	f	f	f	t	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
181	Keg Load	posterior lower	f	f	f	f	f	f	t	hinge	hinge	2026-02-28 12:19:15.622915+00
173	Incline Dumbbell Flyes	anterior upper	f	t	f	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
394	Toes-To-Bars	full body	f	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
182	Kettlebell Figure 8	full body	f	f	t	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
178	Isometric Neck Exercise-Sides	full body	t	f	f	f	f	f	f	carry	isometric	2026-02-28 12:19:15.622915+00
526	Hamstring Stretch	posterior lower	t	f	f	f	f	f	f	hinge	stretch	2026-02-28 12:19:15.622915+00
662	Behind Head Chest Stretch	anterior upper	f	f	f	f	f	f	f	horizontal_push	stretch	2026-02-28 12:19:15.622915+00
184	Kettlebell Pirate Ships	full body	f	f	t	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
395	Wall Walk	full body	f	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
193	Landmine Linear Jammer	full body	f	f	f	t	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
186	Kettlebell Windmill	lower body	t	f	t	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
191	Kneeling Cable Crunch With Alternating Oblique Twists	full body	f	f	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
189	Knee/Hip Raise On Parallel Bars	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
190	Kneeling Arm Drill	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
195	Leverage Shrug	posterior upper	f	f	f	f	t	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
361	Side Leg Raises	lower body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
224	One-Legged Cable Kickback	posterior lower	f	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
197	Linear Acceleration Wall Drill	posterior lower	t	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
194	Latissimus Dorsi-Smr	posterior upper	f	f	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
170	Iliotibial Tract-Smr	lower body	f	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
176	Iron Crosses (Stretch)	anterior lower	t	f	f	f	f	f	f	squat	stretch	2026-02-28 12:19:15.622915+00
201	Low Cable Crossover	anterior upper	f	f	f	f	t	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
203	Lying Close-Grip Barbell Triceps Press To Chin	posterior upper	f	f	f	t	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
58	Wall Slide	posterior upper	t	f	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
603	Plyo Push Up	anterior upper	t	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
73	Ankle Circles	posterior lower	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
596	Lateral Bound	posterior lower	t	f	f	f	f	f	f	carry	plyometric	2026-02-28 12:19:15.622915+00
401	Box Step-Ups	full body	f	t	f	f	f	f	f	lunge	lunge	2026-02-28 12:19:15.622915+00
210	Machine Preacher Curls	anterior upper	f	f	f	f	t	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
556	Ankle Cars	anterior lower	f	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
454	Russian Kettlebell Swings	full body	f	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
244	Pyramid	posterior lower	f	f	f	f	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
316	Wide Stance Stiff Legs	posterior lower	f	f	f	t	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
320	Wrist Roller	anterior upper	f	f	f	t	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
488	Handstand Walk	upper body	f	f	f	f	f	f	f	vertical_push	vertical_push	2026-02-28 12:19:15.622915+00
325	Alternate Leg Diagonal Bound	anterior lower	t	f	f	f	f	f	f	squat	plyometric	2026-02-28 12:19:15.622915+00
383	Double-Unders	full body	f	f	f	f	f	f	f	carry	plyometric	2026-02-28 12:19:15.622915+00
331	Chair Lower Back Stretch	posterior upper	t	f	f	f	f	f	f	horizontal_pull	stretch	2026-02-28 12:19:15.622915+00
393	Thruster	lower body	t	t	t	f	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
404	Hand Release Push Ups	full body	f	f	f	f	f	f	f	horizontal_push	horizontal_push	2026-02-28 12:19:15.622915+00
554	Shoulder Cars	shoulder	f	f	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
555	Thoracic Spine Cars	posterior upper	f	f	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
299	Superman	posterior lower	t	f	f	f	f	f	f	rotation	rotation	2026-02-28 12:19:15.622915+00
309	Toe Touchers	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
310	Tuck Crunch	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
317	Wind Sprints	full body	t	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
75	Anterior Tibialis-Smr	posterior lower	f	f	f	f	f	f	f	carry	carry	2026-02-28 12:19:15.622915+00
645	Power Jerk	anterior lower	f	f	f	t	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
639	Jerk Dip Squat	anterior lower	f	f	f	t	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
643	Overhead Squat	anterior lower	f	f	f	t	f	f	f	squat	squat	2026-02-28 12:19:15.622915+00
644	Power Clean From Blocks	posterior lower	f	f	f	t	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
646	Power Snatch	posterior lower	f	f	f	t	f	f	f	hinge	hinge	2026-02-28 12:19:15.622915+00
667	Crossover Reverse Lunge	posterior lower	t	f	f	f	f	f	f	horizontal_pull	horizontal_pull	2026-02-28 12:19:15.622915+00
\.


--
-- Data for Name: muscles; Type: TABLE DATA; Schema: public; Owner: jacked
--

COPY public.muscles (id, slug, region) FROM stdin;
39	quadriceps	anterior lower
40	hamstrings	posterior lower
41	glutes	posterior lower
42	calves	posterior lower
43	chest	anterior upper
44	lats	posterior upper
45	upper_back	posterior upper
46	rear_delts	posterior upper
47	front_delts	anterior upper
48	side_delts	shoulder
49	biceps	anterior upper
50	triceps	posterior upper
51	forearms	anterior upper
52	core	full body
53	obliques	full body
54	lower_back	posterior lower
55	hip_flexors	anterior lower
56	adductors	anterior lower
57	full_body	full body
58	abductors	posterior lower
59	middle_back	posterior upper
60	neck	posterior upper
\.


--
-- Data for Name: programs_backup_20260226; Type: TABLE DATA; Schema: public; Owner: jacked
--

COPY public.programs_backup_20260226 (id, user_id, start_date, duration_weeks, goal_1, goal_2, goal_3, goal_weight_1, goal_weight_2, goal_weight_3, split_template, days_per_week, progression_style, hybrid_definition, deload_every_n_microcycles, is_active, created_at, is_template, visibility, name, macro_cycle_id, max_session_duration, persona_aggression, persona_tone, generation_in_progress) FROM stdin;
259	1	2026-02-10	10	STRENGTH	HYPERTROPHY	ENDURANCE	10	0	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-09 23:30:21.002311	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
260	22	2026-02-10	12	STRENGTH	HYPERTROPHY	FAT_LOSS	4	3	3	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-09 23:44:09.395179	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
263	22	2026-02-10	12	STRENGTH	FAT_LOSS	HYPERTROPHY	4	6	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-10 01:00:59.477101	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
272	5	2026-02-10	12	STRENGTH	ENDURANCE	HYPERTROPHY	4	6	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-10 21:26:45.422706	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
277	5	2026-02-12	12	STRENGTH	HYPERTROPHY	FAT_LOSS	3	4	3	HYBRID	6	DOUBLE_PROGRESSION	\N	4	f	2026-02-12 00:11:08.06599	f	PRIVATE	Strength + Hypertrophy	\N	75	BALANCED	SUPPORTIVE	f
278	5	2026-02-12	12	HYPERTROPHY	ENDURANCE	FAT_LOSS	3	4	3	HYBRID	6	DOUBLE_PROGRESSION	\N	4	f	2026-02-12 14:30:44.330871	f	PRIVATE	Hypertrophy + endurance + fat loss	\N	75	BALANCED	SUPPORTIVE	f
279	5	2026-02-12	12	HYPERTROPHY	EXPLOSIVENESS	SPEED	4	3	3	HYBRID	6	DOUBLE_PROGRESSION	\N	4	f	2026-02-12 19:26:32.762016	f	PRIVATE	Hypertrophy + explosiveness + speed	\N	90	BALANCED	SUPPORTIVE	f
280	5	2026-02-12	12	HYPERTROPHY	FAT_LOSS	STRENGTH	5	5	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-12 19:38:05.747006	f	PRIVATE	Hypertrophy + fat loss	\N	60	BALANCED	SUPPORTIVE	f
287	5	2026-02-13	12	HYPERTROPHY	ENDURANCE	FAT_LOSS	3	4	3	HYBRID	6	DOUBLE_PROGRESSION	\N	4	f	2026-02-13 10:29:30.962281	f	PRIVATE	Hypertrophy + endurance + fat loss	\N	75	BALANCED	SUPPORTIVE	f
281	5	2026-02-12	12	STRENGTH	ENDURANCE	FAT_LOSS	3	6	1	HYBRID	6	DOUBLE_PROGRESSION	\N	4	f	2026-02-12 20:09:31.063773	f	PRIVATE	Strength + endurance + fat loss	\N	90	BALANCED	SUPPORTIVE	f
282	5	2026-02-12	12	STRENGTH	ENDURANCE	HYPERTROPHY	3	4	3	HYBRID	6	DOUBLE_PROGRESSION	\N	4	f	2026-02-12 20:39:40.902256	f	PRIVATE	Strength + endurance + hypertrophy	\N	120	BALANCED	SUPPORTIVE	f
288	5	2026-02-13	12	STRENGTH	FAT_LOSS	ENDURANCE	2	4	4	HYBRID	6	DOUBLE_PROGRESSION	\N	4	t	2026-02-13 10:42:14.923043	f	PRIVATE	Strength + fat loss + endurance	\N	75	BALANCED	SUPPORTIVE	f
283	5	2026-02-12	12	STRENGTH	ENDURANCE	FAT_LOSS	3	4	3	HYBRID	6	DOUBLE_PROGRESSION	\N	4	f	2026-02-12 21:16:21.448813	f	PRIVATE	Strength + endurance + fat loss	\N	60	BALANCED	SUPPORTIVE	f
284	5	2026-02-12	12	HYPERTROPHY	ENDURANCE	FAT_LOSS	4	2	4	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-12 21:27:25.434589	f	PRIVATE	Hypertrophy + endurance + fat loss	\N	75	BALANCED	SUPPORTIVE	f
261	21	2026-02-10	8	STRENGTH	HYPERTROPHY	ENDURANCE	5	3	2	UPPER_LOWER	4	SINGLE_PROGRESSION	\N	4	f	2026-02-10 00:12:21.708209	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
255	22	2026-02-10	10	STRENGTH	HYPERTROPHY	ENDURANCE	10	0	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-09 23:19:21.33174	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
264	1	2026-02-10	8	STRENGTH	HYPERTROPHY	ENDURANCE	5	3	2	UPPER_LOWER	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-10 01:55:38.119745	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
270	1	2026-02-10	12	STRENGTH	HYPERTROPHY	ENDURANCE	5	5	0	FULL_BODY	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-10 21:05:29.648039	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
274	1	2026-02-12	8	STRENGTH	HYPERTROPHY	ENDURANCE	5	5	0	FULL_BODY	3	DOUBLE_PROGRESSION	\N	4	f	2026-02-12 00:00:38.372064	f	PRIVATE	Test Program - New Flow	\N	60	BALANCED	SUPPORTIVE	f
262	21	2026-02-10	8	STRENGTH	HYPERTROPHY	ENDURANCE	5	3	2	UPPER_LOWER	4	SINGLE_PROGRESSION	\N	4	t	2026-02-10 00:46:34.037038	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
256	22	2026-02-10	10	STRENGTH	HYPERTROPHY	ENDURANCE	10	0	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-09 23:21:06.500886	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
265	5	2026-02-10	12	STRENGTH	ENDURANCE	HYPERTROPHY	5	5	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-10 09:47:46.610661	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
271	22	2026-02-10	12	STRENGTH	HYPERTROPHY	FAT_LOSS	2	5	3	HYBRID	4	DOUBLE_PROGRESSION	\N	4	t	2026-02-10 21:08:13.26879	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
275	1	2026-02-12	8	STRENGTH	HYPERTROPHY	ENDURANCE	5	5	0	FULL_BODY	3	DOUBLE_PROGRESSION	\N	4	f	2026-02-12 00:00:55.474312	f	PRIVATE	Test Program - New Flow	\N	60	BALANCED	SUPPORTIVE	f
257	22	2026-02-10	10	STRENGTH	HYPERTROPHY	ENDURANCE	10	0	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-09 23:27:31.089342	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
266	5	2026-02-10	12	STRENGTH	ENDURANCE	EXPLOSIVENESS	3	4	3	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-10 14:37:29.587646	f	PRIVATE	\N	\N	60	MODERATE_AGGRESSIVE	SUPPORTIVE	f
276	1	2026-02-12	8	STRENGTH	HYPERTROPHY	ENDURANCE	5	5	0	FULL_BODY	3	DOUBLE_PROGRESSION	\N	4	t	2026-02-12 00:01:59.181344	f	PRIVATE	Test Program - New Flow	\N	60	BALANCED	SUPPORTIVE	f
258	22	2026-02-10	10	STRENGTH	HYPERTROPHY	ENDURANCE	10	0	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-09 23:28:51.016783	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
121	1	2026-01-24	12	STRENGTH	HYPERTROPHY	ENDURANCE	5	5	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-24 19:26:39.958444	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
58	1	2026-01-20	12	STRENGTH	ENDURANCE	HYPERTROPHY	5	5	0	UPPER_LOWER	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-20 11:48:54.367446	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
122	1	2026-01-24	12	STRENGTH	HYPERTROPHY	ENDURANCE	5	5	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-24 19:27:01.665896	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
125	1	2026-01-24	12	STRENGTH	ENDURANCE	FAT_LOSS	3	3	4	HYBRID	5	PAUSED_VARIATIONS	\N	4	f	2026-01-24 19:33:11.562483	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
62	1	2026-01-20	12	STRENGTH	ENDURANCE	MOBILITY	4	4	2	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-01-20 13:13:42.262278	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
127	1	2026-01-24	12	STRENGTH	ENDURANCE	FAT_LOSS	3	3	4	HYBRID	5	PAUSED_VARIATIONS	\N	4	f	2026-01-24 19:33:48.850709	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
65	1	2026-01-20	12	ENDURANCE	STRENGTH	HYPERTROPHY	7	3	0	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-01-20 16:07:05.662408	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
129	1	2026-01-24	8	STRENGTH	HYPERTROPHY	ENDURANCE	10	0	0	HYBRID	3	DOUBLE_PROGRESSION	\N	4	f	2026-01-24 19:34:51.39618	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
130	1	2026-01-24	12	STRENGTH	ENDURANCE	FAT_LOSS	1	4	5	HYBRID	5	PAUSED_VARIATIONS	\N	4	f	2026-01-24 19:38:15.863148	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
70	1	2026-01-20	8	STRENGTH	HYPERTROPHY	ENDURANCE	5	3	2	UPPER_LOWER	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-20 22:27:00.374192	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
71	1	2026-01-20	12	STRENGTH	ENDURANCE	FAT_LOSS	3	5	2	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-01-20 22:32:09.530751	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
73	1	2026-01-21	12	STRENGTH	ENDURANCE	FAT_LOSS	3	5	2	PPL	6	DOUBLE_PROGRESSION	\N	4	f	2026-01-20 23:42:50.185556	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
85	1	2026-01-21	12	ENDURANCE	STRENGTH	MOBILITY	5	4	1	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-01-21 16:06:49.410783	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
86	1	2026-01-21	8	STRENGTH	HYPERTROPHY	ENDURANCE	5	3	2	UPPER_LOWER	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-21 16:25:18.324021	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
87	1	2026-01-21	8	HYPERTROPHY	STRENGTH	ENDURANCE	6	4	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-21 16:26:50.766313	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
90	1	2026-01-21	12	ENDURANCE	STRENGTH	HYPERTROPHY	6	4	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-21 16:54:05.97605	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
91	1	2026-01-21	12	ENDURANCE	STRENGTH	HYPERTROPHY	6	4	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-21 18:22:26.555786	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
92	1	2026-01-21	8	STRENGTH	HYPERTROPHY	ENDURANCE	5	3	2	UPPER_LOWER	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-21 18:24:01.372188	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
93	1	2026-01-21	12	STRENGTH	ENDURANCE	FAT_LOSS	1	5	4	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-21 18:30:43.716228	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
95	1	2026-01-23	12	STRENGTH	ENDURANCE	HYPERTROPHY	5	5	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-23 00:16:12.62274	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
97	1	2026-01-23	8	STRENGTH	HYPERTROPHY	ENDURANCE	5	3	2	UPPER_LOWER	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-23 17:44:16.53453	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
1	1	2026-01-15	12	STRENGTH	EXPLOSIVENESS	ENDURANCE	3	3	4	FULL_BODY	5	DOUBLE_PROGRESSION	\N	4	f	2026-01-15 22:11:12.933415	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
98	1	2026-01-23	8	STRENGTH	HYPERTROPHY	ENDURANCE	5	3	2	UPPER_LOWER	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-23 17:44:44.966963	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
113	1	2026-01-24	12	STRENGTH	ENDURANCE	FAT_LOSS	2	4	4	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-01-24 18:34:56.070445	f	PRIVATE	jerome's notes bug	\N	60	BALANCED	SUPPORTIVE	f
116	1	2026-01-24	12	STRENGTH	HYPERTROPHY	ENDURANCE	10	0	0	FULL_BODY	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-24 19:15:39.972171	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
102	1	2026-01-23	12	STRENGTH	ENDURANCE	HYPERTROPHY	4	6	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-23 18:02:06.3821	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
103	1	2026-01-23	12	STRENGTH	ENDURANCE	HYPERTROPHY	4	6	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-23 18:02:10.752598	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
120	1	2026-01-24	12	STRENGTH	HYPERTROPHY	ENDURANCE	5	5	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-24 19:25:57.017611	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
106	1	2026-01-23	8	STRENGTH	HYPERTROPHY	ENDURANCE	5	5	0	FULL_BODY	5	SINGLE_PROGRESSION	\N	4	f	2026-01-23 18:33:20.479892	f	PRIVATE	Test Program	\N	60	BALANCED	SUPPORTIVE	f
123	1	2026-01-24	12	STRENGTH	HYPERTROPHY	ENDURANCE	5	5	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-24 19:30:07.90968	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
124	1	2026-01-24	12	STRENGTH	HYPERTROPHY	ENDURANCE	5	5	0	UPPER_LOWER	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-24 19:31:38.183397	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
126	1	2026-01-24	12	STRENGTH	ENDURANCE	FAT_LOSS	3	3	4	HYBRID	5	PAUSED_VARIATIONS	\N	4	f	2026-01-24 19:33:15.808959	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
128	1	2026-01-24	12	STRENGTH	ENDURANCE	FAT_LOSS	3	3	4	HYBRID	5	PAUSED_VARIATIONS	\N	4	f	2026-01-24 19:34:05.526302	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
131	1	2026-01-24	12	STRENGTH	ENDURANCE	FAT_LOSS	1	4	5	HYBRID	5	PAUSED_VARIATIONS	\N	4	f	2026-01-24 19:38:46.528288	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
108	1	2026-01-23	8	STRENGTH	HYPERTROPHY	ENDURANCE	5	5	0	FULL_BODY	5	DOUBLE_PROGRESSION	\N	4	f	2026-01-23 18:34:10.971942	f	PRIVATE	API Test Program	\N	60	BALANCED	SUPPORTIVE	f
6	1	2026-01-16	12	STRENGTH	ENDURANCE	EXPLOSIVENESS	4	4	2	FULL_BODY	5	DOUBLE_PROGRESSION	\N	4	f	2026-01-15 23:13:46.255168	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
7	1	2026-01-16	12	STRENGTH	ENDURANCE	EXPLOSIVENESS	4	4	2	FULL_BODY	5	DOUBLE_PROGRESSION	\N	4	f	2026-01-15 23:13:50.626456	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
237	5	2026-02-08	12	STRENGTH	ENDURANCE	FAT_LOSS	4	5	1	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-08 12:42:37.183212	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
238	5	2026-02-08	12	STRENGTH	ENDURANCE	FAT_LOSS	4	5	1	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-08 13:02:33.925896	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
239	5	2026-02-08	12	STRENGTH	ENDURANCE	FAT_LOSS	2	4	4	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-08 13:18:59.376555	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
132	1	2026-01-24	12	STRENGTH	ENDURANCE	HYPERTROPHY	6	4	0	HYBRID	4	PAUSED_VARIATIONS	\N	4	f	2026-01-24 19:40:04.103304	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
109	1	2026-01-23	8	STRENGTH	HYPERTROPHY	ENDURANCE	5	5	0	FULL_BODY	5	DOUBLE_PROGRESSION	\N	4	f	2026-01-23 18:37:07.40409	f	PRIVATE	UL program - bookmarked	\N	60	BALANCED	SUPPORTIVE	f
2	1	2026-01-15	12	STRENGTH	EXPLOSIVENESS	ENDURANCE	3	4	3	FULL_BODY	5	DOUBLE_PROGRESSION	\N	4	f	2026-01-15 22:59:25.475257	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
3	1	2026-01-16	12	STRENGTH	EXPLOSIVENESS	ENDURANCE	3	2	5	FULL_BODY	5	DOUBLE_PROGRESSION	\N	4	f	2026-01-15 23:12:27.185235	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
4	1	2026-01-16	12	STRENGTH	EXPLOSIVENESS	ENDURANCE	3	2	5	FULL_BODY	5	DOUBLE_PROGRESSION	\N	4	f	2026-01-15 23:12:34.266427	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
5	1	2026-01-16	12	STRENGTH	EXPLOSIVENESS	ENDURANCE	3	2	5	FULL_BODY	5	DOUBLE_PROGRESSION	\N	4	f	2026-01-15 23:12:44.351233	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
149	5	2026-01-28	12	ENDURANCE	HYPERTROPHY	STRENGTH	7	3	0	HYBRID	6	DOUBLE_PROGRESSION	\N	4	f	2026-01-28 18:26:08.430218	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
150	5	2026-01-29	12	STRENGTH	ENDURANCE	HYPERTROPHY	3	7	0	HYBRID	5	PAUSED_VARIATIONS	\N	4	f	2026-01-29 00:04:51.522547	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
151	5	2026-01-29	12	STRENGTH	ENDURANCE	HYPERTROPHY	3	7	0	HYBRID	5	PAUSED_VARIATIONS	\N	4	f	2026-01-29 00:04:55.979509	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
152	5	2026-01-29	12	STRENGTH	ENDURANCE	HYPERTROPHY	3	7	0	HYBRID	5	PAUSED_VARIATIONS	\N	4	f	2026-01-29 00:08:54.491927	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
153	5	2026-01-29	12	STRENGTH	ENDURANCE	HYPERTROPHY	3	7	0	HYBRID	5	PAUSED_VARIATIONS	\N	4	f	2026-01-29 00:10:20.222921	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
192	20	2026-02-04	8	STRENGTH	HYPERTROPHY	ENDURANCE	10	0	0	PPL	4	SINGLE_PROGRESSION	\N	4	f	2026-02-04 01:53:47.653499	f	PRIVATE	Duration Test Program 75min	\N	75	BALANCED	SUPPORTIVE	f
193	20	2026-02-04	8	STRENGTH	HYPERTROPHY	ENDURANCE	10	0	0	PPL	4	SINGLE_PROGRESSION	\N	4	t	2026-02-04 01:57:01.422179	f	PRIVATE	Duration Test Program 75min	\N	75	BALANCED	SUPPORTIVE	f
148	5	2026-01-28	12	STRENGTH	ENDURANCE	FAT_LOSS	3	5	2	HYBRID	6	DOUBLE_PROGRESSION	\N	4	f	2026-01-28 14:13:39.516995	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
190	5	2026-02-04	12	STRENGTH	ENDURANCE	HYPERTROPHY	4	6	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-04 00:16:36.980587	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
194	5	2026-02-04	12	STRENGTH	ENDURANCE	FAT_LOSS	4	5	1	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-04 09:29:38.949289	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
163	5	2026-01-30	12	STRENGTH	ENDURANCE	FAT_LOSS	2	5	3	HYBRID	6	DOUBLE_PROGRESSION	\N	4	f	2026-01-30 01:34:07.889237	f	PRIVATE	Crossfit circuits working!!	\N	60	BALANCED	SUPPORTIVE	f
168	17	2026-01-31	12	FAT_LOSS	MOBILITY	EXPLOSIVENESS	5	3	2	HYBRID	7	DOUBLE_PROGRESSION	\N	4	t	2026-01-31 15:14:13.269285	f	PRIVATE	\N	\N	90	BALANCED	SUPPORTIVE	f
133	1	2026-01-26	12	STRENGTH	HYPERTROPHY	ENDURANCE	10	0	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-26 01:27:10.855666	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
169	1	2026-02-02	12	STRENGTH	FAT_LOSS	HYPERTROPHY	4	4	2	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-02 22:15:50.92327	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
170	1	2026-02-02	12	STRENGTH	FAT_LOSS	HYPERTROPHY	4	4	2	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-02 22:20:20.076439	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
171	1	2026-02-02	12	STRENGTH	ENDURANCE	FAT_LOSS	4	5	1	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-02 22:37:34.147379	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
195	5	2026-02-04	12	STRENGTH	ENDURANCE	SPEED	3	5	2	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-04 12:07:44.968552	f	PRIVATE	\N	\N	75	BALANCED	SUPPORTIVE	f
180	5	2026-02-03	12	STRENGTH	FAT_LOSS	HYPERTROPHY	5	5	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-03 20:47:45.500458	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
181	5	2026-02-03	12	STRENGTH	FAT_LOSS	HYPERTROPHY	5	5	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-03 20:48:04.000257	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
182	5	2026-02-03	12	STRENGTH	ENDURANCE	HYPERTROPHY	4	6	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-03 21:36:17.969746	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
183	5	2026-02-03	12	STRENGTH	ENDURANCE	HYPERTROPHY	3	7	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-03 21:40:49.939194	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
184	5	2026-02-03	12	STRENGTH	MOBILITY	ENDURANCE	3	2	5	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-03 22:04:35.570895	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
186	19	2026-02-04	8	HYPERTROPHY	STRENGTH	ENDURANCE	5	3	2	FULL_BODY	4	SINGLE_PROGRESSION	\N	4	f	2026-02-04 00:07:00.371231	f	PRIVATE	Test Session Generation Fix	\N	60	BALANCED	SUPPORTIVE	f
187	19	2026-02-04	8	HYPERTROPHY	STRENGTH	ENDURANCE	5	3	2	FULL_BODY	4	SINGLE_PROGRESSION	\N	4	f	2026-02-04 00:08:18.404097	f	PRIVATE	Test Session Generation Fix	\N	60	BALANCED	SUPPORTIVE	f
188	19	2026-02-04	8	HYPERTROPHY	STRENGTH	ENDURANCE	5	3	2	FULL_BODY	4	SINGLE_PROGRESSION	\N	4	f	2026-02-04 00:09:51.091668	f	PRIVATE	Test Session Generation Fix	\N	60	BALANCED	SUPPORTIVE	f
189	19	2026-02-04	8	HYPERTROPHY	STRENGTH	ENDURANCE	5	3	2	FULL_BODY	4	SINGLE_PROGRESSION	\N	4	t	2026-02-04 00:12:11.284205	f	PRIVATE	Test Session Generation Fix	\N	60	BALANCED	SUPPORTIVE	f
185	5	2026-02-03	12	STRENGTH	ENDURANCE	HYPERTROPHY	5	5	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-03 22:54:23.669086	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
196	5	2026-02-04	12	STRENGTH	ENDURANCE	MOBILITY	4	5	1	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-04 14:26:53.796895	f	PRIVATE	\N	\N	75	BALANCED	SUPPORTIVE	f
197	5	2026-02-04	12	STRENGTH	ENDURANCE	HYPERTROPHY	4	6	0	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-04 15:04:20.593444	f	PRIVATE	\N	\N	75	BALANCED	SUPPORTIVE	f
198	5	2026-02-04	12	STRENGTH	ENDURANCE	HYPERTROPHY	4	5	1	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-04 19:57:33.522254	f	PRIVATE	\N	\N	75	BALANCED	SUPPORTIVE	f
199	5	2026-02-04	12	STRENGTH	ENDURANCE	HYPERTROPHY	5	5	0	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-04 21:55:41.941813	f	PRIVATE	\N	\N	75	BALANCED	SUPPORTIVE	f
177	1	2026-02-03	12	STRENGTH	ENDURANCE	HYPERTROPHY	4	6	0	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-03 08:30:08.454163	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
200	5	2026-02-05	12	STRENGTH	HYPERTROPHY	EXPLOSIVENESS	4	5	1	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-04 23:29:38.561741	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
202	5	2026-02-05	12	STRENGTH	ENDURANCE	HYPERTROPHY	5	5	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-05 00:24:41.041043	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
203	5	2026-02-05	12	STRENGTH	ENDURANCE	MOBILITY	4	5	1	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-05 08:39:35.688959	f	PRIVATE	\N	\N	75	BALANCED	SUPPORTIVE	f
8	1	2026-01-16	12	STRENGTH	ENDURANCE	EXPLOSIVENESS	4	4	2	FULL_BODY	5	DOUBLE_PROGRESSION	\N	4	f	2026-01-15 23:14:00.836709	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
43	1	2026-01-20	8	HYPERTROPHY	STRENGTH	ENDURANCE	5	5	0	FULL_BODY	3	DOUBLE_PROGRESSION	\N	4	f	2026-01-20 00:20:28.606522	f	PRIVATE	Debug Program	\N	60	BALANCED	SUPPORTIVE	f
191	20	2026-02-04	8	STRENGTH	HYPERTROPHY	ENDURANCE	10	0	0	PPL	4	SINGLE_PROGRESSION	\N	4	f	2026-02-04 01:52:00.416015	f	PRIVATE	Duration Test Program 75min	\N	75	BALANCED	SUPPORTIVE	f
9	1	2026-01-16	12	STRENGTH	ENDURANCE	EXPLOSIVENESS	4	4	2	FULL_BODY	5	DOUBLE_PROGRESSION	\N	4	f	2026-01-15 23:15:34.034674	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
11	1	2026-01-16	12	STRENGTH	FAT_LOSS	ENDURANCE	3	4	3	FULL_BODY	5	DOUBLE_PROGRESSION	\N	4	f	2026-01-15 23:23:32.197326	f	PRIVATE	My New Program	\N	60	BALANCED	SUPPORTIVE	f
12	1	2026-01-16	12	STRENGTH	FAT_LOSS	ENDURANCE	3	4	3	FULL_BODY	5	DOUBLE_PROGRESSION	\N	4	f	2026-01-15 23:23:43.24901	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
114	1	2026-01-24	12	ENDURANCE	FAT_LOSS	STRENGTH	5	4	1	HYBRID	5	PAUSED_VARIATIONS	\N	4	f	2026-01-24 19:12:48.389769	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
115	1	2026-01-24	12	ENDURANCE	FAT_LOSS	STRENGTH	5	4	1	HYBRID	5	PAUSED_VARIATIONS	\N	4	f	2026-01-24 19:12:52.765226	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
22	1	2026-01-16	12	EXPLOSIVENESS	MOBILITY	ENDURANCE	3	2	5	FULL_BODY	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-16 20:40:07.584259	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
117	1	2026-01-24	12	ENDURANCE	FAT_LOSS	EXPLOSIVENESS	5	3	2	HYBRID	5	PAUSED_VARIATIONS	\N	4	f	2026-01-24 19:22:57.622541	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
38	1	2026-01-19	12	STRENGTH	ENDURANCE	MOBILITY	3	4	3	FULL_BODY	5	DOUBLE_PROGRESSION	\N	4	f	2026-01-18 23:39:35.915357	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
118	1	2026-01-24	12	ENDURANCE	FAT_LOSS	EXPLOSIVENESS	5	3	2	HYBRID	5	PAUSED_VARIATIONS	\N	4	f	2026-01-24 19:23:02.30352	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
119	1	2026-01-24	12	STRENGTH	HYPERTROPHY	ENDURANCE	5	5	0	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-24 19:24:13.545925	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
42	1	2026-01-20	12	ENDURANCE	FAT_LOSS	STRENGTH	5	5	0	FULL_BODY	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-20 00:00:34.095637	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
47	1	2026-01-20	8	HYPERTROPHY	STRENGTH	ENDURANCE	5	5	0	UPPER_LOWER	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-20 01:29:33.777436	f	PRIVATE	Test Program	\N	60	BALANCED	SUPPORTIVE	f
56	1	2026-01-20	12	STRENGTH	HYPERTROPHY	ENDURANCE	5	3	2	UPPER_LOWER	4	DOUBLE_PROGRESSION	\N	4	f	2026-01-20 10:45:50.229622	f	PRIVATE	Reproduction Program	\N	60	BALANCED	SUPPORTIVE	f
228	1	2026-02-06	12	STRENGTH	ENDURANCE	FAT_LOSS	2	3	5	HYBRID	6	DOUBLE_PROGRESSION	\N	4	f	2026-02-06 15:51:40.394395	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
240	5	2026-02-08	12	STRENGTH	ENDURANCE	FAT_LOSS	3	2	5	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-08 14:35:01.322535	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
224	1	2026-02-06	12	STRENGTH	FAT_LOSS	HYPERTROPHY	4	6	0	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-06 02:17:00.330699	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
217	5	2026-02-06	12	STRENGTH	ENDURANCE	HYPERTROPHY	3	5	2	HYBRID	6	DOUBLE_PROGRESSION	\N	4	f	2026-02-06 00:39:32.316357	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
218	5	2026-02-06	12	HYPERTROPHY	STRENGTH	ENDURANCE	1	4	5	HYBRID	6	DOUBLE_PROGRESSION	\N	4	f	2026-02-06 01:21:02.943566	f	PRIVATE	\N	\N	75	BALANCED	SUPPORTIVE	f
201	1	2026-02-05	8	STRENGTH	HYPERTROPHY	ENDURANCE	5	3	2	UPPER_LOWER	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-05 00:18:18.506146	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
209	1	2026-02-05	12	STRENGTH	ENDURANCE	EXPLOSIVENESS	2	6	2	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-05 21:29:29.532239	f	PRIVATE	\N	\N	75	BALANCED	SUPPORTIVE	f
226	5	2026-02-06	12	STRENGTH	ENDURANCE	FAT_LOSS	1	5	4	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-06 11:33:04.738717	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
214	5	2026-02-06	12	FAT_LOSS	MOBILITY	STRENGTH	6	4	0	HYBRID	6	DOUBLE_PROGRESSION	\N	4	f	2026-02-05 23:26:14.576229	f	PRIVATE	\N	\N	75	BALANCED	SUPPORTIVE	f
212	1	2026-02-05	12	ENDURANCE	EXPLOSIVENESS	FAT_LOSS	4	4	2	HYBRID	6	DOUBLE_PROGRESSION	\N	4	f	2026-02-05 21:56:06.551363	f	PRIVATE	\N	\N	75	BALANCED	SUPPORTIVE	f
220	1	2026-02-06	12	STRENGTH	ENDURANCE	MOBILITY	2	5	3	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-06 02:10:35.835927	f	PRIVATE	\N	\N	75	BALANCED	SUPPORTIVE	f
221	1	2026-02-06	12	STRENGTH	ENDURANCE	MOBILITY	3	5	2	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-06 02:14:01.057456	f	PRIVATE	\N	\N	75	BALANCED	SUPPORTIVE	f
222	1	2026-02-06	12	STRENGTH	ENDURANCE	MOBILITY	4	4	2	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-06 02:15:16.762995	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
223	1	2026-02-06	12	STRENGTH	ENDURANCE	HYPERTROPHY	3	7	0	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-06 02:16:08.595686	f	PRIVATE	\N	\N	75	BALANCED	SUPPORTIVE	f
219	5	2026-02-06	12	STRENGTH	ENDURANCE	MOBILITY	3	5	2	HYBRID	6	DOUBLE_PROGRESSION	\N	4	f	2026-02-06 01:40:52.763251	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
225	5	2026-02-06	12	STRENGTH	ENDURANCE	MOBILITY	3	5	2	HYBRID	4	DOUBLE_PROGRESSION	\N	4	f	2026-02-06 11:30:12.692493	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
227	5	2026-02-06	12	STRENGTH	FAT_LOSS	ENDURANCE	2	4	4	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-06 14:31:12.414224	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
229	5	2026-02-07	12	ENDURANCE	FAT_LOSS	EXPLOSIVENESS	4	3	3	HYBRID	6	DOUBLE_PROGRESSION	\N	4	f	2026-02-06 23:46:39.360136	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
232	5	2026-02-07	12	STRENGTH	ENDURANCE	FAT_LOSS	1	5	4	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-07 16:15:54.892126	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
235	5	2026-02-08	12	STRENGTH	ENDURANCE	HYPERTROPHY	4	6	0	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-08 12:26:25.835359	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
236	5	2026-02-08	12	STRENGTH	ENDURANCE	FAT_LOSS	2	5	3	HYBRID	5	DOUBLE_PROGRESSION	\N	4	f	2026-02-08 12:38:41.306606	f	PRIVATE	\N	\N	60	BALANCED	SUPPORTIVE	f
\.


--
-- Data for Name: tags; Type: TABLE DATA; Schema: public; Owner: jacked
--

COPY public.tags (id, name) FROM stdin;
101	strength
102	cardio
103	stretching
104	athleticism
105	rehabilitation
106	explosiveness
107	plyometrics
108	olympic
109	hypertrophy
110	endurance
111	mobility
112	isometric
113	speed
114	crossfit
115	athletic
117	olympic_lifting
122	posterior_chain
123	compound
124	full_body
125	fundamental
126	quad_dominant
127	anterior_chain
128	chest_dominant
129	upper_body
130	back_dominant
131	bodyweight
132	supinated_grip
133	shoulder_dominant
134	explosive
135	power
\.


--
-- Name: activity_definitions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jacked
--

SELECT pg_catalog.setval('public.activity_definitions_id_seq', 1, false);


--
-- Name: activity_muscle_map_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jacked
--

SELECT pg_catalog.setval('public.activity_muscle_map_id_seq', 1, false);


--
-- Name: circuits_melted_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jacked
--

SELECT pg_catalog.setval('public.circuits_melted_id_seq', 1, false);


--
-- Name: equipment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jacked
--

SELECT pg_catalog.setval('public.equipment_id_seq', 1, false);


--
-- Name: hyrox_scraping_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jacked
--

SELECT pg_catalog.setval('public.hyrox_scraping_log_id_seq', 1, true);


--
-- Name: hyrox_scraping_log_staging_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jacked
--

SELECT pg_catalog.setval('public.hyrox_scraping_log_staging_id_seq', 2, true);


--
-- Name: hyrox_workout_lines_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jacked
--

SELECT pg_catalog.setval('public.hyrox_workout_lines_id_seq', 45, true);


--
-- Name: hyrox_workout_movements_staging_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jacked
--

SELECT pg_catalog.setval('public.hyrox_workout_movements_staging_id_seq', 1, false);


--
-- Name: hyrox_workout_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jacked
--

SELECT pg_catalog.setval('public.hyrox_workout_tags_id_seq', 5, true);


--
-- Name: hyrox_workouts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jacked
--

SELECT pg_catalog.setval('public.hyrox_workouts_id_seq', 5, true);


--
-- Name: movement_coaching_cues_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jacked
--

SELECT pg_catalog.setval('public.movement_coaching_cues_id_seq', 200, true);


--
-- Name: movement_muscle_map_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jacked
--

SELECT pg_catalog.setval('public.movement_muscle_map_id_seq', 34, true);


--
-- Name: movements_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jacked
--

SELECT pg_catalog.setval('public.movements_id_seq', 717, true);


--
-- Name: muscles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jacked
--

SELECT pg_catalog.setval('public.muscles_id_seq', 1, false);


--
-- Name: tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jacked
--

SELECT pg_catalog.setval('public.tags_id_seq', 1, false);


--
-- Name: activity_definitions activity_definitions_pkey; Type: CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.activity_definitions
    ADD CONSTRAINT activity_definitions_pkey PRIMARY KEY (id);


--
-- Name: activity_muscle_map activity_muscle_map_pkey; Type: CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.activity_muscle_map
    ADD CONSTRAINT activity_muscle_map_pkey PRIMARY KEY (id);


--
-- Name: circuits_melted circuits_melted_pkey; Type: CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.circuits_melted
    ADD CONSTRAINT circuits_melted_pkey PRIMARY KEY (id);


--
-- Name: equipment equipment_pkey; Type: CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.equipment
    ADD CONSTRAINT equipment_pkey PRIMARY KEY (id);


--
-- Name: hyrox_scraping_log hyrox_scraping_log_pkey; Type: CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.hyrox_scraping_log
    ADD CONSTRAINT hyrox_scraping_log_pkey PRIMARY KEY (id);


--
-- Name: hyrox_scraping_log hyrox_scraping_log_scrape_session_id_key; Type: CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.hyrox_scraping_log
    ADD CONSTRAINT hyrox_scraping_log_scrape_session_id_key UNIQUE (scrape_session_id);


--
-- Name: hyrox_scraping_log_staging hyrox_scraping_log_staging_pkey; Type: CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.hyrox_scraping_log_staging
    ADD CONSTRAINT hyrox_scraping_log_staging_pkey PRIMARY KEY (id);


--
-- Name: hyrox_workout_lines hyrox_workout_lines_pkey; Type: CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.hyrox_workout_lines
    ADD CONSTRAINT hyrox_workout_lines_pkey PRIMARY KEY (id);


--
-- Name: hyrox_workout_movements_staging hyrox_workout_movements_staging_pkey; Type: CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.hyrox_workout_movements_staging
    ADD CONSTRAINT hyrox_workout_movements_staging_pkey PRIMARY KEY (id);


--
-- Name: hyrox_workout_tags hyrox_workout_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.hyrox_workout_tags
    ADD CONSTRAINT hyrox_workout_tags_pkey PRIMARY KEY (id);


--
-- Name: hyrox_workouts hyrox_workouts_pkey; Type: CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.hyrox_workouts
    ADD CONSTRAINT hyrox_workouts_pkey PRIMARY KEY (id);


--
-- Name: hyrox_workouts hyrox_workouts_wod_id_key; Type: CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.hyrox_workouts
    ADD CONSTRAINT hyrox_workouts_wod_id_key UNIQUE (wod_id);


--
-- Name: migration_version migration_version_pkey; Type: CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.migration_version
    ADD CONSTRAINT migration_version_pkey PRIMARY KEY (version);


--
-- Name: movement_coaching_cues movement_coaching_cues_pkey; Type: CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.movement_coaching_cues
    ADD CONSTRAINT movement_coaching_cues_pkey PRIMARY KEY (id);


--
-- Name: movement_muscle_map movement_muscle_map_pkey; Type: CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.movement_muscle_map
    ADD CONSTRAINT movement_muscle_map_pkey PRIMARY KEY (id);


--
-- Name: movements_backup_20260228 movements_backup_20260228_pkey; Type: CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.movements_backup_20260228
    ADD CONSTRAINT movements_backup_20260228_pkey PRIMARY KEY (id);


--
-- Name: movements movements_pkey; Type: CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.movements
    ADD CONSTRAINT movements_pkey PRIMARY KEY (id);


--
-- Name: muscles muscles_pkey; Type: CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.muscles
    ADD CONSTRAINT muscles_pkey PRIMARY KEY (id);


--
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (id);


--
-- Name: hyrox_workout_lines uq_hyrox_workout_lines_line; Type: CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.hyrox_workout_lines
    ADD CONSTRAINT uq_hyrox_workout_lines_line UNIQUE (workout_id, line_number);


--
-- Name: hyrox_workout_tags uq_hyrox_workout_tags_workout_tag; Type: CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.hyrox_workout_tags
    ADD CONSTRAINT uq_hyrox_workout_tags_workout_tag UNIQUE (workout_id, tag_name);


--
-- Name: idx_hyrox_scraping_log_created_at; Type: INDEX; Schema: public; Owner: jacked
--

CREATE INDEX idx_hyrox_scraping_log_created_at ON public.hyrox_scraping_log USING btree (created_at);


--
-- Name: idx_hyrox_scraping_log_session_id; Type: INDEX; Schema: public; Owner: jacked
--

CREATE INDEX idx_hyrox_scraping_log_session_id ON public.hyrox_scraping_log USING btree (scrape_session_id);


--
-- Name: idx_hyrox_scraping_log_staging_session; Type: INDEX; Schema: public; Owner: jacked
--

CREATE INDEX idx_hyrox_scraping_log_staging_session ON public.hyrox_scraping_log_staging USING btree (scrape_session_id);


--
-- Name: idx_hyrox_workout_lines_is_rest; Type: INDEX; Schema: public; Owner: jacked
--

CREATE INDEX idx_hyrox_workout_lines_is_rest ON public.hyrox_workout_lines USING btree (is_rest);


--
-- Name: idx_hyrox_workout_lines_movement_id; Type: INDEX; Schema: public; Owner: jacked
--

CREATE INDEX idx_hyrox_workout_lines_movement_id ON public.hyrox_workout_lines USING btree (movement_id);


--
-- Name: idx_hyrox_workout_lines_workout_id; Type: INDEX; Schema: public; Owner: jacked
--

CREATE INDEX idx_hyrox_workout_lines_workout_id ON public.hyrox_workout_lines USING btree (workout_id);


--
-- Name: idx_hyrox_workout_movements_staging_workout; Type: INDEX; Schema: public; Owner: jacked
--

CREATE INDEX idx_hyrox_workout_movements_staging_workout ON public.hyrox_workout_movements_staging USING btree (workout_id);


--
-- Name: idx_hyrox_workout_tags_tag_name; Type: INDEX; Schema: public; Owner: jacked
--

CREATE INDEX idx_hyrox_workout_tags_tag_name ON public.hyrox_workout_tags USING btree (tag_name);


--
-- Name: idx_hyrox_workout_tags_workout_id; Type: INDEX; Schema: public; Owner: jacked
--

CREATE INDEX idx_hyrox_workout_tags_workout_id ON public.hyrox_workout_tags USING btree (workout_id);


--
-- Name: idx_hyrox_workouts_name; Type: INDEX; Schema: public; Owner: jacked
--

CREATE INDEX idx_hyrox_workouts_name ON public.hyrox_workouts USING btree (name);


--
-- Name: idx_hyrox_workouts_wod_id; Type: INDEX; Schema: public; Owner: jacked
--

CREATE INDEX idx_hyrox_workouts_wod_id ON public.hyrox_workouts USING btree (wod_id);


--
-- Name: idx_movements_backup_20260228_id; Type: INDEX; Schema: public; Owner: jacked
--

CREATE INDEX idx_movements_backup_20260228_id ON public.movements_backup_20260228 USING btree (id);


--
-- Name: idx_movements_pattern_subtype; Type: INDEX; Schema: public; Owner: jacked
--

CREATE INDEX idx_movements_pattern_subtype ON public.movements USING btree (pattern_subtype);


--
-- Name: hyrox_workout_lines fk_hyrox_workout_lines_movement_id; Type: FK CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.hyrox_workout_lines
    ADD CONSTRAINT fk_hyrox_workout_lines_movement_id FOREIGN KEY (movement_id) REFERENCES public.movements(id) ON DELETE SET NULL;


--
-- Name: hyrox_workout_lines fk_hyrox_workout_lines_workout_id; Type: FK CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.hyrox_workout_lines
    ADD CONSTRAINT fk_hyrox_workout_lines_workout_id FOREIGN KEY (workout_id) REFERENCES public.hyrox_workouts(id) ON DELETE CASCADE;


--
-- Name: hyrox_workout_tags fk_hyrox_workout_tags_workout_id; Type: FK CONSTRAINT; Schema: public; Owner: jacked
--

ALTER TABLE ONLY public.hyrox_workout_tags
    ADD CONSTRAINT fk_hyrox_workout_tags_workout_id FOREIGN KEY (workout_id) REFERENCES public.hyrox_workouts(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict Zusjb51QfU1quAagXkcYO27QhN8UsU0Ofqfw0fWSBvvSPjxmCxNmfGPkdpTWiDv

