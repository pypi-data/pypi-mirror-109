from typing import List

import numpy as np
from negmas import Contract

from scml.scml2020.common import NO_COMMAND

__all__ = [
    "ProductionStrategy",
    "SupplyDrivenProductionStrategy",
    "DemandDrivenProductionStrategy",
    "TradeDrivenProductionStrategy",
]


class ProductionStrategy:
    """Represents a strategy for controlling production."""


class SupplyDrivenProductionStrategy(ProductionStrategy):
    """A production strategy that converts all inputs to outputs

    Hooks Into:
        - `step`

    Remarks:
        - `Attributes` section describes the attributes that can be used to construct the component (passed to its
          `__init__` method).
        - `Provides` section describes the attributes (methods, properties, data-members) made available by this
          component directly. Note that everything provided by the bases of this components are also available to the
          agent (Check the `Bases` section above for all the bases of this component).
        - `Requires` section describes any requirements from the agent using this component. It defines a set of methods
          or properties/data-members that must exist in the agent that uses this component. These requirement are
          usually implemented as abstract methods in the component
        - `Abstract` section describes abstract methods that MUST be implemented by any descendant of this component.
        - `Hooks Into` section describes the methods this component overrides calling `super` () which allows other
          components to hook into the same method (by overriding it). Usually callbacks starting with `on_` are
          hooked into this way.
        - `Overrides` section describes the methods this component overrides without calling `super` effectively
          disallowing any other components after it in the MRO to call this method. Usually methods that do some
          action (i.e. not starting with `on_`) are overridden this way.
    """

    def step(self):
        super().step()
        # start by assuming we are not going to produce anything
        commands = NO_COMMAND * np.ones(self.awi.n_lines, dtype=int)
        # find the number of input product items we have
        inputs = min(self.awi.state.inventory[self.awi.my_input_product], len(commands))
        # produce all items of input product found in the inventory
        commands[:inputs] = self.awi.my_input_product
        commands[inputs:] = NO_COMMAND
        # issue production command
        self.awi.set_commands(commands)


class DemandDrivenProductionStrategy(ProductionStrategy):
    """A production strategy that produces ONLY when a contract is secured

    Hooks Into:
        - `on_contract_finalized`

    Remarks:
        - `Attributes` section describes the attributes that can be used to construct the component (passed to its
          `__init__` method).
        - `Provides` section describes the attributes (methods, properties, data-members) made available by this
          component directly. Note that everything provided by the bases of this components are also available to the
          agent (Check the `Bases` section above for all the bases of this component).
        - `Requires` section describes any requirements from the agent using this component. It defines a set of methods
          or properties/data-members that must exist in the agent that uses this component. These requirement are
          usually implemented as abstract methods in the component
        - `Abstract` section describes abstract methods that MUST be implemented by any descendant of this component.
        - `Hooks Into` section describes the methods this component overrides calling `super` () which allows other
          components to hook into the same method (by overriding it). Usually callbacks starting with `on_` are
          hooked into this way.
        - `Overrides` section describes the methods this component overrides without calling `super` effectively
          disallowing any other components after it in the MRO to call this method. Usually methods that do some
          action (i.e. not starting with `on_`) are overridden this way.
    """

    def on_contracts_finalized(
        self: "SCML2020Agent",
        signed: List[Contract],
        cancelled: List[Contract],
        rejectors: List[List[str]],
    ) -> None:
        super().on_contracts_finalized(signed, cancelled, rejectors)
        # register production for guaranteed sales
        for contract in signed:
            # if this is not a sale contract, ignore it
            is_seller = contract.annotation["seller"] == self.id
            if not is_seller:
                continue
            # find the day at which I should deliver the item. I must produce
            # at most one day earlier
            step = contract.agreement["time"]
            # find the earliest time I can do anything about this contract
            earliest_production = self.awi.current_step
            # if there is no time to produce for this contract, ignore it
            if step > self.awi.n_steps - 1 or step < earliest_production:
                continue
            output_product = contract.annotation["product"]
            # Find the process index to generate my output product
            process = output_product - 1
            # schedule production to end at most one day before delivery time
            steps, _ = self.awi.schedule_production(
                process=process,
                repeats=contract.agreement["quantity"],
                step=(earliest_production, step - 1),
                line=-1,
                partial_ok=True,
            )


class TradeDrivenProductionStrategy(ProductionStrategy):
    """A production strategy that produces ONLY for contracts that the agent did not initiate.

    Provides:
        - `schedule_range` : A mapping from contract ID to a tuple of the first
          and last steps at which some lines are occupied to produce the
          quantity specified by the contract and whether it is a sell contract

    Hooks Into:
        - `on_contract_finalized`

    Remarks:
        - `Attributes` section describes the attributes that can be used to construct the component (passed to its
          `__init__` method).
        - `Provides` section describes the attributes (methods, properties, data-members) made available by this
          component directly. Note that everything provided by the bases of this components are also available to the
          agent (Check the `Bases` section above for all the bases of this component).
        - `Requires` section describes any requirements from the agent using this component. It defines a set of methods
          or properties/data-members that must exist in the agent that uses this component. These requirement are
          usually implemented as abstract methods in the component
        - `Abstract` section describes abstract methods that MUST be implemented by any descendant of this component.
        - `Hooks Into` section describes the methods this component overrides calling `super` () which allows other
          components to hook into the same method (by overriding it). Usually callbacks starting with `on_` are
          hooked into this way.
        - `Overrides` section describes the methods this component overrides without calling `super` effectively
          disallowing any other components after it in the MRO to call this method. Usually methods that do some
          action (i.e. not starting with `on_`) are overridden this way.
    """

    def on_contracts_finalized(
        self: "SCML2020Agent",
        signed: List[Contract],
        cancelled: List[Contract],
        rejectors: List[List[str]],
    ) -> None:
        super().on_contracts_finalized(signed, cancelled, rejectors)
        for contract in signed:
            # ignore contracts that resulted from negotiations I initiated
            if contract.annotation["caller"] == self.id:
                continue
            # find whether the contract is a sale or procurement contract
            is_seller = contract.annotation["seller"] == self.id
            # find the day of delivery
            step = contract.agreement["time"]
            # find the earliest time I can do anything about this contract
            earliest_production = self.awi.current_step
            if step > self.awi.n_steps - 1 or step < earliest_production:
                continue
            # if I am a seller, I will schedule production
            output_product = contract.annotation["product"]
            input_product = output_product - 1
            # schedule production to finish one day before delivery for sales
            # and to start on the same day of delivery for procurement.
            # Note that for procurement, we need to finish production at least
            # one day before the last step (n_steps-2) to have one step for
            # selling
            self.awi.schedule_production(
                process=input_product,
                repeats=contract.agreement["quantity"],
                step=(earliest_production, step - 1)
                if is_seller
                else (step, self.awi.n_steps - 2),
                line=-1,
                partial_ok=True,
            )
