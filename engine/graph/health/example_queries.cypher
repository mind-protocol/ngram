// =============================================================================
// THE BLOOD LEDGER - Example Cypher Queries
// Natural language-inspired queries for FalkorDB
// Quality ratings indicate gameplay/narrative usefulness (1-10)
// =============================================================================
// DOCS: docs/schema/graph-health/PATTERNS_Graph_Health_Validation.md

// -----------------------------------------------------------------------------
// CHARACTER QUERIES
// -----------------------------------------------------------------------------

// Who is at York right now?
// Quality: 9/10 - Essential for scene setup, used constantly
MATCH (c:Actor)-[at:AT]->(p:Space {name: 'York'})
WHERE at.present > 0.5
RETURN c.name, c.type, at.visible

// All living companions and their current locations
// Quality: 10/10 - Core gameplay, player needs this constantly
MATCH (c:Actor {type: 'companion', alive: true})-[at:AT]->(p:Space)
WHERE at.present > 0.5
RETURN c.name, p.name AS location, at.visible AS visible

// Characters hiding (present but not visible)
// Quality: 8/10 - Great for drama, ambushes, dramatic reveals
MATCH (c:Actor)-[at:AT]->(p:Space)
WHERE at.present > 0.5 AND at.visible < 0.5
RETURN c.name AS hidden_character, p.name AS hiding_at

// Normans vs Saxons - characters by faction (inferred from narratives)
// Quality: 7/10 - Useful for faction dynamics, but indirect inference
MATCH (c:Actor)-[b:BELIEVES]->(n:Narrative)
WHERE n.content CONTAINS 'Norman' AND b.believes > 0.7
RETURN DISTINCT c.name AS norman_sympathizer

// Characters who have witnessed something (not just heard)
// Quality: 8/10 - Distinguishes reliable from unreliable sources
MATCH (c:Actor)-[b:BELIEVES {source: 'witnessed'}]->(n:Narrative)
RETURN c.name, n.name, n.content

// Characters with a specific flaw
// Quality: 6/10 - Useful for character-driven scenes, less urgent
MATCH (c:Actor)
WHERE c.flaw = 'doubt'
RETURN c.name, c.backstory_wound

// The cunning ones - characters with cunning approach
// Quality: 6/10 - Good for predicting behavior, planning encounters
MATCH (c:Actor {approach: 'cunning'})
RETURN c.name, c.voice_tone, c.flaw

// Dead characters and how they died (via narratives)
// Quality: 7/10 - Important for consequences, memorial scenes
MATCH (c:Actor {alive: false})
OPTIONAL MATCH (n:Narrative)-[]->(c)
WHERE n.type = 'memory'
RETURN c.name, c.type, n.content AS death_story


// -----------------------------------------------------------------------------
// KNOWLEDGE & BELIEFS
// -----------------------------------------------------------------------------

// What does Aldric know? (All narratives with heard > 0.5)
// Quality: 10/10 - Core mechanic, determines what companions can share
MATCH (c:Actor {name: 'Aldric'})-[b:BELIEVES]->(n:Narrative)
WHERE b.heard > 0.5
RETURN n.name, n.content, b.believes AS certainty, b.source

// Who knows about the oath sworn to Gospatric?
// Quality: 9/10 - Tracks narrative spread, crucial for story
MATCH (c:Actor)-[b:BELIEVES]->(n:Narrative)
WHERE n.name CONTAINS 'oath' AND b.heard > 0.5
RETURN c.name, b.believes AS how_certain, b.source AS how_learned

// Secrets - narratives that characters are hiding
// Quality: 10/10 - Drama gold, revelation opportunities
MATCH (c:Actor)-[b:BELIEVES]->(n:Narrative)
WHERE b.hides > 0.5
RETURN c.name AS keeper, n.name AS secret, n.content

// Conflicting beliefs - characters who doubt what they've heard
// Quality: 8/10 - Internal conflict, roleplay opportunities
MATCH (c:Actor)-[b:BELIEVES]->(n:Narrative)
WHERE b.heard > 0.5 AND b.doubts > 0.3
RETURN c.name, n.name, b.believes, b.doubts AS doubt_level

// Who originated this narrative? (The original source)
// Quality: 9/10 - Track rumors to source, verify information
MATCH (c:Actor)-[b:BELIEVES]->(n:Narrative)
WHERE b.originated > 0.8
RETURN n.name AS narrative, c.name AS original_source

// Narrative spread - who told whom
// Quality: 8/10 - Information network visualization
MATCH (c:Actor)-[b:BELIEVES]->(n:Narrative)
WHERE b.source = 'told' AND b.from_whom IS NOT NULL
RETURN c.name AS learned_by, n.name, b.from_whom AS told_by

// False beliefs - what characters believe that isn't true
// Quality: 10/10 - Dramatic irony, player vs character knowledge
MATCH (c:Actor)-[b:BELIEVES]->(n:Narrative)
WHERE b.believes > 0.7 AND n.truth < 0.3
RETURN c.name AS believer, n.name AS false_belief, n.truth AS actual_truth

// Common knowledge - narratives believed by 3+ characters
// Quality: 7/10 - Establishes "what everyone knows"
MATCH (c:Actor)-[b:BELIEVES]->(n:Narrative)
WHERE b.believes > 0.5
WITH n, count(c) AS believers
WHERE believers >= 3
RETURN n.name, n.content, believers
ORDER BY believers DESC


// -----------------------------------------------------------------------------
// PLACE & GEOGRAPHY
// -----------------------------------------------------------------------------

// All places by type
// Quality: 5/10 - Reference/debugging, not gameplay
MATCH (p:Space)
RETURN p.type, collect(p.name) AS places
ORDER BY p.type

// River crossings - strategic choke points
// Quality: 8/10 - Military planning, ambush locations
MATCH (p:Space)
WHERE p.type = 'crossing'
RETURN p.name, p.detail

// What's within a day's travel from York? (path_hours < 24)
// Quality: 9/10 - Essential for travel planning
MATCH (york:Space {name: 'York'})-[c:CONNECTS]-(nearby:Space)
WHERE c.path > 0 AND c.path_hours < 24
RETURN nearby.name, c.path_hours AS hours_away, c.path_terrain AS terrain

// Roman roads - fast travel routes
// Quality: 8/10 - Strategic movement, Norman patrol routes
MATCH (p1:Space)-[c:CONNECTS {path_terrain: 'roman_road'}]->(p2:Space)
RETURN p1.name AS from_place, p2.name AS to_place, c.path_km AS km

// Dangerous paths through wilderness
// Quality: 7/10 - Risk/reward travel choices
MATCH (p1:Space)-[c:CONNECTS]->(p2:Space)
WHERE c.path_terrain IN ['moor', 'forest', 'marsh']
RETURN p1.name, p2.name, c.path_terrain, c.path_hours

// Hidden camps and outlaw hideouts
// Quality: 9/10 - Resistance network, safe houses
MATCH (p:Space)
WHERE p.type IN ['camp', 'ruin']
RETURN p.name, p.type, p.detail

// Places with dark or fearful mood
// Quality: 7/10 - Atmosphere, horror/suspense scenes
MATCH (p:Space)
WHERE p.mood IN ['fearful', 'hostile', 'desperate']
RETURN p.name, p.mood, p.detail


// -----------------------------------------------------------------------------
// THINGS & POSSESSIONS
// -----------------------------------------------------------------------------

// What is Malet carrying?
// Quality: 9/10 - NPC inventory, what can be taken/stolen
MATCH (c:Actor)-[r:CARRIES]->(t:Thing)
WHERE c.name CONTAINS 'Malet' AND r.carries > 0.5
RETURN t.name, t.type, t.significance, r.carries_hidden AS hidden

// All legendary items and their locations
// Quality: 10/10 - Quest objects, major plot items
MATCH (t:Thing {significance: 'legendary'})
OPTIONAL MATCH (t)-[l:LOCATED_AT]->(p:Space)
OPTIONAL MATCH (c:Actor)-[r:CARRIES]->(t)
RETURN t.name, t.description,
       CASE WHEN p IS NOT NULL THEN p.name ELSE null END AS at_place,
       CASE WHEN c IS NOT NULL THEN c.name ELSE null END AS carried_by

// Sacred relics and who guards them
// Quality: 9/10 - Religious power, leverage over church
MATCH (t:Thing {significance: 'sacred'})
OPTIONAL MATCH (c:Actor)-[r:CARRIES]->(t)
WHERE r.carries > 0.5
RETURN t.name, c.name AS guardian

// Hidden treasures - things concealed at places
// Quality: 9/10 - Discovery, loot, secrets
MATCH (t:Thing)-[l:LOCATED_AT]->(p:Space)
WHERE l.hidden > 0.5
RETURN t.name, p.name AS hidden_at, l.specific_location

// Political documents - who controls the paperwork
// Quality: 8/10 - Legitimacy, forgery opportunities
MATCH (t:Thing {type: 'document', significance: 'political'})
OPTIONAL MATCH (c:Actor)-[r:CARRIES]->(t)
RETURN t.name, t.description, c.name AS held_by

// Weapons in play
// Quality: 7/10 - Combat preparation, disarmament
MATCH (t:Thing {type: 'weapon'})
OPTIONAL MATCH (c:Actor)-[r:CARRIES]->(t)
OPTIONAL MATCH (t)-[l:LOCATED_AT]->(p:Space)
RETURN t.name, t.significance,
       c.name AS carried_by, p.name AS located_at

// Provisions and supplies - survival resources
// Quality: 6/10 - Logistics, siege/winter survival
MATCH (t:Thing {type: 'provisions'})
OPTIONAL MATCH (t)-[l:LOCATED_AT]->(p:Space)
RETURN t.name, t.quantity, p.name AS location


// -----------------------------------------------------------------------------
// NARRATIVES
// -----------------------------------------------------------------------------

// Oaths - binding promises that constrain behavior
// Quality: 9/10 - Character motivation, obligation tracking
MATCH (n:Narrative {type: 'oath'})
RETURN n.name, n.content, n.tone, n.about_characters

// Blood feuds and enmities
// Quality: 9/10 - Conflict drivers, revenge plots
MATCH (n:Narrative)
WHERE n.type IN ['enmity', 'blood']
RETURN n.name, n.content, n.about_relationship

// Debts owed - who owes what to whom
// Quality: 8/10 - Leverage, obligation, favor economy
MATCH (n:Narrative {type: 'debt'})
RETURN n.name, n.content, n.about_characters

// Where did events happen? (Narratives linked to places)
// Quality: 8/10 - Historical significance of locations
MATCH (n:Narrative)-[:OCCURRED_AT]->(p:Space)
RETURN n.name, n.content, p.name AS location

// Contradicting narratives - stories in conflict
// Quality: 9/10 - Mystery, unreliable narrators, truth-seeking
MATCH (n1:Narrative)-[r:NARRATIVE_LINK]->(n2:Narrative)
WHERE r.contradicts > 0.5
RETURN n1.name AS story_a, n2.name AS story_b, r.contradicts AS conflict

// Rumors spreading through the North
// Quality: 8/10 - Information warfare, propaganda
MATCH (n:Narrative {type: 'rumor'})
MATCH (c:Actor)-[b:BELIEVES]->(n)
WHERE b.spreads > 0.5
RETURN n.name, n.content, collect(c.name) AS spreading_it

// Secrets that could destroy someone
// Quality: 10/10 - Blackmail, revelation, dramatic bombs
MATCH (n:Narrative {type: 'secret'})
RETURN n.name, n.content, n.about_characters, n.truth


// -----------------------------------------------------------------------------
// COMPLEX RELATIONSHIP QUERIES
// -----------------------------------------------------------------------------

// Who knows what about whom?
// Quality: 9/10 - Character web, who can betray whom
MATCH (knower:Actor)-[b:BELIEVES]->(n:Narrative)
WHERE n.about_characters IS NOT NULL AND b.heard > 0.5
RETURN knower.name AS knows, n.name AS the_story, n.about_characters AS about

// Characters at same location with conflicting beliefs
// Quality: 10/10 - Confrontation setup, dramatic conflict
MATCH (c1:Actor)-[at1:AT]->(p:Space)<-[at2:AT]-(c2:Actor)
WHERE at1.present > 0.5 AND at2.present > 0.5 AND c1 <> c2
MATCH (c1)-[b1:BELIEVES]->(n:Narrative)<-[b2:BELIEVES]-(c2)
WHERE b1.believes > 0.7 AND b2.denies > 0.5
RETURN p.name AS location, c1.name AS believer, c2.name AS denier, n.name AS disputed

// The information brokers - who knows the most
// Quality: 8/10 - Key NPCs for information gathering
MATCH (c:Actor)-[b:BELIEVES]->(n:Narrative)
WHERE b.heard > 0.5
WITH c, count(n) AS knowledge_count
RETURN c.name, knowledge_count
ORDER BY knowledge_count DESC
LIMIT 10

// Isolated characters - present but knowing little
// Quality: 7/10 - Vulnerable targets, uninformed actors
MATCH (c:Actor)-[at:AT]->(p:Space)
WHERE at.present > 0.5
WITH c
MATCH (c)-[b:BELIEVES]->(n:Narrative)
WITH c, count(n) AS knowledge_count
WHERE knowledge_count < 3
RETURN c.name AS isolated_character, knowledge_count

// Power brokers - characters who originated many narratives
// Quality: 8/10 - Influential figures, narrative shapers
MATCH (c:Actor)-[b:BELIEVES]->(n:Narrative)
WHERE b.originated > 0.8
WITH c, count(n) AS narratives_created
WHERE narratives_created > 1
RETURN c.name, narratives_created
ORDER BY narratives_created DESC

// Shared secrets - characters who both know a hidden thing
// Quality: 9/10 - Conspiracy detection, trust networks
MATCH (c1:Actor)-[b1:BELIEVES]->(n:Narrative)<-[b2:BELIEVES]-(c2:Actor)
WHERE b1.hides > 0.5 AND b2.hides > 0.5 AND c1 <> c2
RETURN n.name AS shared_secret, c1.name, c2.name


// -----------------------------------------------------------------------------
// GAMEPLAY QUERIES (Scene Setup)
// -----------------------------------------------------------------------------

// Scene setup: Who is here and what do they know?
// Quality: 10/10 - Run this at every scene start
MATCH (c:Actor)-[at:AT]->(p:Space {name: 'York'})
WHERE at.present > 0.5
WITH c, at
OPTIONAL MATCH (c)-[b:BELIEVES]->(n:Narrative)
WHERE b.heard > 0.5
RETURN c.name, c.type, at.visible AS visible,
       collect(n.name) AS knows_about

// What can the player learn here? (From present NPCs)
// Quality: 10/10 - Conversation opportunities
MATCH (player:Actor {type: 'player'})-[at:AT]->(p:Space)
WHERE at.present > 0.5
WITH p
MATCH (npc:Actor)-[at2:AT]->(p)
WHERE at2.present > 0.5 AND npc.type <> 'player'
MATCH (npc)-[b:BELIEVES]->(n:Narrative)
WHERE b.heard > 0.5 AND b.hides < 0.5
RETURN DISTINCT n.name, n.content, collect(DISTINCT npc.name) AS who_can_tell

// Travel options from current location
// Quality: 9/10 - Movement decisions
MATCH (current:Space {name: 'York'})-[c:CONNECTS]->(dest:Space)
WHERE c.path > 0
RETURN dest.name, dest.type, c.path_hours AS hours, c.path_terrain AS route
ORDER BY c.path_hours

// Things of interest at location
// Quality: 8/10 - Interactive objects, loot
MATCH (p:Space {name: 'York'})<-[l:LOCATED_AT]-(t:Thing)
WHERE l.located > 0.5 AND l.hidden < 0.5
RETURN t.name, t.type, t.significance, t.description

// Companion status check
// Quality: 10/10 - Party management
MATCH (c:Actor {type: 'companion', alive: true})
OPTIONAL MATCH (c)-[at:AT]->(p:Space)
WHERE at.present > 0.5
RETURN c.name, c.voice_tone, c.approach, c.flaw, p.name AS location

// Who might betray us? (Characters with conflicting loyalties)
// Quality: 8/10 - Trust assessment, paranoia fuel
MATCH (c:Actor)-[b1:BELIEVES]->(n1:Narrative)
MATCH (c)-[b2:BELIEVES]->(n2:Narrative)
WHERE b1.believes > 0.5 AND b2.believes > 0.5
  AND n1.type = 'oath' AND n2.type = 'oath'
  AND n1 <> n2
RETURN c.name, n1.name AS oath_1, n2.name AS oath_2


// -----------------------------------------------------------------------------
// ATMOSPHERIC QUERIES
// -----------------------------------------------------------------------------

// Holy ground - sacred sites for sanctuary or oaths
// Quality: 7/10 - Ritual locations, safe havens
MATCH (p:Space)
WHERE p.type IN ['abbey', 'monastery', 'holy_well', 'standing_stones']
RETURN p.name, p.type, p.detail

// Norman strongholds - enemy territory
// Quality: 8/10 - Danger zones, infiltration targets
MATCH (p:Space {type: 'hold'})
RETURN p.name, p.detail

// The wild places - hiding spots
// Quality: 7/10 - Escape routes, outlaw territory
MATCH (p:Space)
WHERE p.type IN ['forest', 'wilderness']
RETURN p.name, p.detail

// Armed characters - who's dangerous
// Quality: 7/10 - Threat assessment
MATCH (c:Actor)-[r:CARRIES]->(t:Thing {type: 'weapon'})
WHERE r.carries > 0.5
RETURN c.name, t.name, c.type, c.alive

// The weather of war - place moods across the north
// Quality: 6/10 - Atmosphere, regional pressure mapping
MATCH (p:Space)
WHERE p.mood IS NOT NULL
RETURN p.mood, collect(p.name) AS places
ORDER BY p.mood


// -----------------------------------------------------------------------------
// DEBUGGING & HEALTH CHECKS
// -----------------------------------------------------------------------------

// Count all nodes by type
// Quality: 4/10 - Technical debugging only
MATCH (n)
RETURN labels(n)[0] AS type, count(n) AS count
ORDER BY count DESC

// Count all relationships by type
// Quality: 4/10 - Technical debugging only
MATCH ()-[r]->()
RETURN type(r) AS relationship, count(r) AS count
ORDER BY count DESC

// Orphan nodes (no relationships) - data quality issue
// Quality: 5/10 - Data cleanup, should be empty
MATCH (n)
WHERE NOT (n)--()
RETURN labels(n)[0] AS type, n.id, n.name

// Characters without locations - broken state
// Quality: 5/10 - Should be empty, fix if not
MATCH (c:Actor)
WHERE NOT (c)-[:AT]->(:Space)
RETURN c.name, c.type

// Things floating in void - need location or carrier
// Quality: 5/10 - Data quality check
MATCH (t:Thing)
WHERE NOT (t)-[:LOCATED_AT]->(:Space) AND NOT (:Actor)-[:CARRIES]->(t)
RETURN t.name, t.type

// Narratives no one knows - orphan stories
// Quality: 5/10 - Wasted content, connect or remove
MATCH (n:Narrative)
WHERE NOT (:Actor)-[:BELIEVES]->(n)
RETURN n.name, n.type

// Schema validation - characters with invalid types
// Quality: 4/10 - Data quality enforcement
MATCH (c:Actor)
WHERE NOT c.type IN ['player', 'companion', 'major', 'minor', 'background']
RETURN c.name, c.type AS invalid_type
