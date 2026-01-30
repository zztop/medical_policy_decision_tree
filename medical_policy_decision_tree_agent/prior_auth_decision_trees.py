from pydantic import BaseModel, Field


class PriorAuthDecisionTree(BaseModel):
    medical_condition: str = Field(description="Name of the rule")
    brief_description: str = Field(
        description="One line description of the medical condition"
    )
    decision_tree: str = Field(
        description="Decision tree to list out all the criteria's needed to determine if a prior authorization required"
    )


class PriorAuthDecisionTrees(BaseModel):
    # pa_decision_tree_name: str = Field(
    #     description="Name of the prior authorization decision tree"
    # )
    pa_decision_trees: list[PriorAuthDecisionTree] = Field(
        description="List of all prior authorization decision rules"
    )
