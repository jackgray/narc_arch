

import { Database, aql } from "arangojs";

const db = new Database();

(async function() {
    const now = Date.now();
    
    try { 
        const cursor = await db.query(aql 
             RETURN ${now}
            );
    } catch (err) {
        console.log("Error during query")
    }
    
})();