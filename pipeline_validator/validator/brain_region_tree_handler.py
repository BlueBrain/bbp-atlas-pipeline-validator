from bigtree import Node, list_to_tree_by_relation, find_name


class BrainRegionTreeHandler:
    def __init__(self, brain_regions) -> None:
        self.tree = self.__brain_regions_to_tree(brain_regions)

    @staticmethod
    def __brain_regions_to_tree(brain_regions) -> Node:
        """
        Converts the brain regions to a bigtree structure
        :param brain_regions:
        :return:
        """
        brain_region_relationships = []
        for brain_region in brain_regions:
            parentId = (
                brain_region["isPartOf"][0] if "isPartOf" in brain_region else None
            )
            brain_region_id = brain_region["@id"]
            if (
                parentId
                and brain_region_id
                and "http://api.brain-map.org/api/v2/data/Structure" in brain_region_id
                and "http://api.brain-map.org/api/v2/data/Structure" in parentId
            ):
                brain_region_relationships.append((parentId, brain_region_id))
        root = list_to_tree_by_relation(brain_region_relationships)
        return root

    def check_ancestry_order_between_regions(
        self, previous_brain_region: str, check_node: Node
    ) -> bool:
        """
        Checks the ancestry order between two regions
        :param previous_brain_region: the id of the previous brain region
        :param check_node: the node we are currently checking
        :return:
        """
        previous_node = find_name(self.tree, previous_brain_region)
        # if the node we are checking appears in the ancestry before its previous, the ancestry is incorrect
        if check_node.name in previous_node.path_name:
            return False
        return True
