from models import DatasetLineage

def creates_cycle(db, upstream_id, downstream_id):
    visited = set()

    def dfs(node_id):
        if node_id == upstream_id:
            return True
        visited.add(node_id)
        children = db.query(DatasetLineage)\
            .filter_by(upstream_id=node_id).all()
        for c in children:
            if c.downstream_id not in visited:
                if dfs(c.downstream_id):
                    return True
        return False

    return dfs(downstream_id)