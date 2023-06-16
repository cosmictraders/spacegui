# Search Docs
## Usage
`[name]: [comparison] [value]`
## Comparisons
- `=` - used by default when no other comparison is detected meaning you can leave it out of the query, and it will be assumed.
- `<`, `>`, `<=`, `>=` - used when comparing integers and floats
## General Filters
- `is` - Filter by type i.e. `is: system`. Possible values are `system`, `waypoint`, `ship`, and `all`.
## System Filters
- `type` - Filter by star type
- `waypoints` - Filter by number of waypoints. For example, use `waypoints:>0` to search for all systems with at least one waypoint. 
- `x` - Filter by x coordinate
- `y` - Filter by y coordinate
## Waypoint Filters
- `type` - Filter by waypoint type
- `trait` search for individual trait or multiple traits seperated by commas with no spaces.
- `system` - Filter by system
- `x` - Filter by x coordinate
- `y` - Filter by y coordinate

## Ship Filters
- `type` - Filter by ship role (`ship.registration.role`)
- `status` - Nav status (i.e. `IN_TRANSIT`, `ORBITING`, or `DOCKED`)
- `fuel` - Filter by the raw value of the ships current fuel
- `cargo` - Filter by the raw value of the ships current cargo
- `waypoint` - Filter by ship waypoint location
- `system` - Filter by ship system location
