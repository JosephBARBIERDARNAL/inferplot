import matplotlib.pyplot as plt
import matplotlib
import narwhals as nw
from narwhals.typing import IntoDataFrame
from typing import Union
import scipy.stats as st
import numpy as np

from inferplot._utils import _infer_types
from inferplot.utils import themify

np.random.seed(0)


class BetweenStats:
    @classmethod
    def fit(
        cls,
        x: str,
        y: str,
        data: IntoDataFrame,
        orientation: str = "vertical",
        paired: bool = False,
        colors: list = None,
        plot_violin: bool = True,
        plot_box: bool = True,
        plot_scatter: bool = True,
        violin_kws: Union[dict, None] = None,
        box_kws: Union[dict, None] = None,
        scatter_kws: Union[dict, None] = None,
        ax: Union[matplotlib.axes.Axes, None] = None,
        **kwargs,
    ):
        if orientation not in ["vertical", "horizontal"]:
            raise ValueError(
                "orientation argument must be one of: 'vertical', 'horizontal'."
            )

        df = nw.from_native(data)
        cat_col, num_col = _infer_types(x, y, df)
        result = [sub_df[num_col].to_list() for _, sub_df in df.group_by(cat_col)]
        sample_sizes = [len(sub_df) for _, sub_df in df.group_by(cat_col)]
        cat_labels = df[cat_col].unique().to_list()
        n_cat = df[cat_col].n_unique()
        n = len(data)

        if colors is None:
            colors = plt.rcParams["axes.prop_cycle"].by_key()["color"][:n_cat]
        else:
            if len(colors) < n_cat:
                raise ValueError(
                    f"`colors` argument must have at least {n_cat} elements, not {len(colors)}"
                )
        if ax is None:
            ax = plt.gca()
        if violin_kws is None:
            violin_kws = {}
        if box_kws is None:
            box_kws = {}
        if scatter_kws is None:
            scatter_kws = {}
        violin_default_kws = {"orientation": orientation, "showextrema": False}
        violin_default_kws.update(violin_kws)
        box_default_kws = {"orientation": orientation}
        box_default_kws.update(box_kws)
        scatter_default_kws = {"alpha": 0.5}
        scatter_default_kws.update(box_kws)

        if plot_violin:
            violin_artists = ax.violinplot(result, **violin_default_kws)

        if plot_box:
            box_style = {"color": "#3b3b3b"}
            ax.boxplot(
                result,
                boxprops=box_style,
                medianprops=box_style,
                capprops=box_style,
                whiskerprops=box_style,
                **box_default_kws,
            )

        if plot_scatter:
            for i, (values, label, color) in enumerate(zip(result, cat_labels, colors)):
                jitter = np.random.uniform(low=-0.1, high=0.1, size=len(values))
                x_coords = np.full(len(values), i) + jitter + 1
                if orientation == "vertical":
                    ax.scatter(x_coords, values, color=color, **scatter_default_kws)
                else:  # "horizontal"
                    ax.scatter(values, x_coords, color=color, **scatter_default_kws)

        for patch, color in zip(violin_artists["bodies"], colors):
            patch.set(color=color)

        if n_cat < 2:
            raise ValueError(
                "You must have at least 2 distinct categories in your category column"
            )
        elif n_cat == 2:
            cls.is_ANOVA = False
            if paired:
                ttest = st.ttest_rel(result[0], result[1])
                cls.name = "Paired t-test"
            else:
                ttest = st.ttest_ind(result[0], result[1])
                cls.name = "T-test"
            statistic = ttest.statistic
            pvalue = ttest.pvalue
            dof = int(ttest.df)
            cls.dof = dof
            main_stat = f"t_{{Student}}({dof}) = {statistic:.2f}"
        else:  # n >= 3
            cls.is_ANOVA = True
            if paired:
                raise NotImplementedError(
                    "Repeated measures ANOVA has not been implemented yet."
                )
            else:
                anova = st.f_oneway(*result)
                cls.name = "One-way ANOVA"
            statistic = anova.statistic
            pvalue = anova.pvalue
            dof_between = n_cat - 1
            dof_within = n - n_cat
            cls.dof_between = dof_between
            cls.dof_within = dof_within
            main_stat = f"F({dof_between}, {dof_within}) = {statistic:.2f}"

        expr_list = [
            "$",
            f"{main_stat}, ",
            f"p = {pvalue:.4f}, ",
            f"n_{{obs}} = {n}",
            "$",
        ]

        all_expr = "".join(expr_list)

        annotation_params = dict(transform=ax.transAxes, va="top")
        ax.text(x=0.05, y=1.09, s=all_expr, size=9, **annotation_params)

        ax = themify(ax)

        ticks = [i + 1 for i in range(len(sample_sizes))]
        labels = [f"{label}\nn = {n}" for n, label in zip(sample_sizes, cat_labels)]
        if orientation == "vertical":
            ax.set_xticks(ticks, labels=labels)
        elif orientation == "horizontal":
            ax.set_yticks(ticks, labels=labels)

        cls.statistic = statistic
        cls.pvalue = pvalue
        cls.main_stat = main_stat
        cls.ax = ax
        cls.is_paired = paired
        cls.expression = all_expr
        cls.n_cat = n_cat
        cls.n_obs = n
        cls._is_fitted = True

        return cls

    @classmethod
    def summary(cls):
        if not hasattr(cls, "_is_fitted"):
            raise RuntimeError("Must call 'fit()' before calling 'summary()'.")

        print("Between stats comparison\n")

        info_about_test = [
            f"{cls.name} ",
            f"with {cls.n_cat} groups" if cls.is_ANOVA else "",
        ]
        info_about_test = "".join(info_about_test)

        clean_expression = (
            cls.expression.replace("$", "").replace("{", "").replace("}", "")
        )
        print(f"Test: {info_about_test}")
        print(clean_expression)


if __name__ == "__main__":
    from inferplot import datasets

    data = datasets.load_iris()
    data = data[data["species"] != "setosa"]

    fig, ax = plt.subplots()
    bs = BetweenStats.fit(
        data=data,
        x="species",
        y="sepal_length",
        orientation="vertical",
        ax=ax,
    )
    bs.summary()
    fig.savefig("cache.png", dpi=300, bbox_inches="tight")
