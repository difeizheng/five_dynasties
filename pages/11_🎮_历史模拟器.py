"""
🎮 历史模拟器
"如果...会怎样"式的历史推演工具
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import json


st.set_page_config(page_title="历史模拟器", page_icon="🎮", layout="wide")


# ============================================
# 模拟器核心逻辑
# ============================================

def init_simulator_state():
    """初始化模拟器状态"""
    if "simulator_scenarios" not in st.session_state:
        st.session_state["simulator_scenarios"] = []


def create_scenario(
    name: str,
    description: str,
    changes: dict,
    outcome: str
) -> dict:
    """创建推演场景"""
    return {
        "id": f"scenario_{len(st.session_state['simulator_scenarios']) + 1}",
        "name": name,
        "description": description,
        "changes": changes,
        "outcome": outcome,
        "created_at": datetime.now().isoformat(),
    }


def save_scenario(scenario: dict):
    """保存推演场景"""
    init_simulator_state()
    st.session_state["simulator_scenarios"].append(scenario)


def get_all_scenarios() -> list:
    """获取所有推演场景"""
    init_simulator_state()
    return st.session_state["simulator_scenarios"]


def delete_scenario(scenario_id: str):
    """删除推演场景"""
    init_simulator_state()
    st.session_state["simulator_scenarios"] = [
        s for s in st.session_state["simulator_scenarios"] if s["id"] != scenario_id
    ]


def clear_all_scenarios():
    """清空所有场景"""
    init_simulator_state()
    st.session_state["simulator_scenarios"] = []


def export_scenarios() -> str:
    """导出推演场景"""
    init_simulator_state()
    return json.dumps(st.session_state["simulator_scenarios"], indent=2, ensure_ascii=False)


def import_scenarios(json_str: str) -> tuple[int, int]:
    """导入推演场景"""
    init_simulator_state()
    try:
        data = json.loads(json_str)
        imported_count = 0
        skipped_count = 0

        for scenario in data:
            if "id" not in scenario:
                continue

            # 检查是否已存在
            exists = any(s["id"] == scenario["id"] for s in st.session_state["simulator_scenarios"])
            if not exists:
                st.session_state["simulator_scenarios"].append(scenario)
                imported_count += 1
            else:
                skipped_count += 1

        return imported_count, skipped_count
    except:
        return 0, 0


# ============================================
# 推演逻辑
# ============================================

def simulate_regime_longevity(regime: str, base_years: int, factor: float) -> int:
    """模拟政权存续时间"""
    return int(base_years * factor)


def simulate_battle_outcome(
    attacker_power: int,
    defender_power: int,
    luck_factor: float = 1.0
) -> dict:
    """模拟战役结果"""
    attacker_score = attacker_power * luck_factor
    defender_score = defender_power

    if attacker_score > defender_score * 1.2:
        winner = "attacker"
        confidence = min(95, int((attacker_score - defender_score) / defender_score * 100))
    elif defender_score > attacker_score * 1.2:
        winner = "defender"
        confidence = min(95, int((defender_score - attacker_score) / attacker_score * 100))
    else:
        winner = "stalemate"
        confidence = 50

    return {
        "winner": winner,
        "confidence": confidence,
        "attacker_score": int(attacker_score),
        "defender_score": int(defender_score),
    }


def simulate_unification_probability(
    regime_power: int,
    rival_powers: list,
    diplomacy_factor: float = 1.0
) -> float:
    """模拟统一概率"""
    total_rival_power = sum(rival_powers)
    adjusted_power = regime_power * diplomacy_factor

    if total_rival_power == 0:
        return 100.0

    probability = (adjusted_power / (adjusted_power + total_rival_power)) * 100
    return min(99, max(1, probability))


# ============================================
# UI 组件
# ============================================

def render_scenario_card(scenario: dict):
    """渲染场景卡片"""
    with st.expander(f"📜 {scenario['name']}"):
        st.markdown(f"**描述**: {scenario['description']}")

        st.markdown("**假设条件**:")
        for key, value in scenario["changes"].items():
            st.markdown(f"- {key}: {value}")

        st.markdown(f"**推演结果**: {scenario['outcome']}")
        st.caption(f"创建时间：{scenario['created_at']}")

        if st.button("🗑️ 删除", key=f"del_{scenario['id']}"):
            delete_scenario(scenario["id"])
            st.rerun()


def render_header():
    """渲染页面头部"""
    st.title("🎮 历史模拟器")
    st.markdown("""
    **历史模拟器** - 探索"如果...会怎样"的历史可能性

    在这里你可以：
    - 🤔 调整历史参数，探索不同的历史走向
    - ⚔️ 模拟战役结果，改变政权命运
    - 🌍 推演统一进程，重写历史结局
    - 💾 保存和分享你的推演场景
    """)
    st.markdown("---")


def render_power_simulator():
    """政权实力模拟器"""
    st.subheader("⚔️ 政权实力对比模拟器")

    st.markdown("调整各政权的实力参数，模拟不同的历史走向")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**你的政权**")
        my_regime = st.selectbox(
            "选择政权",
            ["后周", "南唐", "后唐", "前蜀", "后蜀", "南汉", "吴越"],
            key="sim_my_regime"
        )
        my_power = st.slider("实力值", 0, 100, 70, key="sim_my_power")
        diplomacy = st.slider("外交关系", 0, 100, 50, help="越高表示与其他政权关系越好", key="sim_diplomacy")

    with col2:
        st.markdown("**主要对手**")
        rival_regime = st.selectbox(
            "选择主要对手",
            ["后周", "南唐", "后唐", "前蜀", "后蜀", "南汉", "吴越"],
            key="sim_rival_regime"
        )
        rival_power = st.slider("对手实力", 0, 100, 60, key="sim_rival_power")

    if st.button("🎯 开始推演"):
        if my_regime == rival_regime:
            st.warning("请选择不同的政权")
        else:
            # 计算统一概率
            rivals = [rival_power, 50, 40, 30]  # 简化：其他政权实力
            diplomacy_factor = 1 + (diplomacy - 50) / 100
            probability = simulate_unification_probability(my_power, rivals, diplomacy_factor)

            st.markdown("### 📊 推演结果")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("统一概率", f"{probability:.1f}%")
            with col2:
                st.metric("实力对比", f"{my_power}:{rival_power}")
            with col3:
                advantage = "优势" if my_power > rival_power else "劣势"
                st.metric("局势评估", advantage)

            # 保存场景
            outcome = f"{my_regime}统一概率为{probability:.1f}%"
            scenario = create_scenario(
                name=f"{my_regime} vs {rival_regime}",
                description=f"如果{my_regime}的实力为{my_power}，外交关系为{diplomacy}",
                changes={
                    f"{my_regime}实力": my_power,
                    f"{rival_regime}实力": rival_power,
                    "外交关系": diplomacy,
                },
                outcome=outcome,
            )

            if st.button("💾 保存此场景"):
                save_scenario(scenario)
                st.success("场景已保存")


def render_battle_simulator():
    """战役模拟器"""
    st.subheader("🗡️ 战役模拟器")

    st.markdown("模拟特定战役的结果")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**进攻方**")
        attacker = st.text_input("进攻方名称", "后周", key="battle_attacker")
        attacker_power = st.slider("进攻方实力", 0, 100, 60, key="battle_attacker_power")

    with col2:
        st.markdown("**防守方**")
        defender = st.text_input("防守方名称", "南唐", key="battle_defender")
        defender_power = st.slider("防守方实力", 0, 100, 50, key="battle_defender_power")

    luck = st.slider("运气因素", 0.5, 2.0, 1.0, 0.1, help="1.0 为正常，<1.0 为不利，>1.0 为有利", key="battle_luck")

    if st.button("⚔️ 模拟战役"):
        result = simulate_battle_outcome(attacker_power, defender_power, luck)

        st.markdown("### 📊 战役结果")

        if result["winner"] == "attacker":
            st.success(f"🏆 **{attacker}** 获胜！")
        elif result["winner"] == "defender":
            st.error(f"🛡️ **{defender}** 守住了！")
        else:
            st.warning("🤝 双方僵持不下")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(f"{attacker}得分", result["attacker_score"])
        with col2:
            st.metric(f"{defender}得分", result["defender_score"])

        st.progress(result["confidence"] / 100)
        st.caption(f"结果置信度：{result['confidence']}%")

        # 保存场景
        outcome = f"{attacker} vs {defender}: {result['winner']}获胜"
        scenario = create_scenario(
            name=f"{attacker} vs {defender} 战役",
            description=f"模拟{attacker}进攻{defender}的战役",
            changes={
                "进攻方实力": attacker_power,
                "防守方实力": defender_power,
                "运气因素": luck,
            },
            outcome=outcome,
        )

        if st.button("💾 保存此场景", key="save_battle"):
            save_scenario(scenario)
            st.success("场景已保存")


def render_timeline_simulator():
    """时间线推演"""
    st.subheader("📅 政权存续时间推演")

    st.markdown("调整历史参数，推演政权可能的存续时间")

    regime = st.selectbox(
        "选择政权",
        ["后梁", "后唐", "后晋", "后汉", "后周", "吴越", "南唐", "前蜀", "后蜀", "南汉", "楚", "闽国", "荆南", "北汉"],
        key="timeline_regime"
    )

    # 各政权基础存续时间
    base_durations = {
        "后梁": 17, "后唐": 14, "后晋": 11, "后汉": 4, "后周": 10,
        "吴越": 72, "南唐": 39, "前蜀": 18, "后蜀": 31, "南汉": 55,
        "楚": 44, "闽国": 36, "荆南": 40, "北汉": 29,
    }

    base_duration = base_durations.get(regime, 10)

    st.info(f"历史实际存续时间：**{base_duration} 年**")

    st.markdown("**影响因素**:")

    col1, col2 = st.columns(2)

    with col1:
        ruler_quality = st.slider("君主能力", 1, 10, 5, help="1=昏君，10=明君")
        economy = st.slider("经济发展", 1, 10, 5)

    with col2:
        military = st.slider("军事实力", 1, 10, 5)
        diplomacy = st.slider("外交环境", 1, 10, 5, help="1=四面受敌，10=友邦环绕")

    if st.button("🔮 推演"):
        # 计算综合因素
        factor = (ruler_quality + economy + military + diplomacy) / 20
        simulated_duration = simulate_regime_longevity(regime, base_duration, factor)

        st.markdown("### 📊 推演结果")

        delta = simulated_duration - base_duration
        delta_str = f"+{delta}" if delta > 0 else str(delta)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("原存续时间", f"{base_duration}年")
        with col2:
            st.metric("推演存续时间", f"{simulated_duration}年", delta_str)
        with col3:
            change = "延长" if delta > 0 else "缩短"
            st.metric("变化", change)

        if delta > 5:
            st.success("🎉 政权显著延长！")
        elif delta > 0:
            st.success("✅ 政权有所延长")
        elif delta < -5:
            st.error("⚠️ 政权显著缩短！")
        else:
            st.warning("📊 变化不大")

        # 保存场景
        outcome = f"{regime}存续{simulated_duration}年（原{base_duration}年）"
        scenario = create_scenario(
            name=f"{regime}存续推演",
            description=f"推演{regime}在不同条件下的存续时间",
            changes={
                "君主能力": ruler_quality,
                "经济发展": economy,
                "军事实力": military,
                "外交环境": diplomacy,
            },
            outcome=outcome,
        )

        if st.button("💾 保存此场景", key="save_timeline"):
            save_scenario(scenario)
            st.success("场景已保存")


def render_scenario_manager():
    """场景管理器"""
    st.subheader("💾 推演场景管理")

    scenarios = get_all_scenarios()

    if not scenarios:
        st.info("暂无保存的推演场景")
    else:
        st.markdown(f"共 {len(scenarios)} 个场景")

        for scenario in scenarios:
            render_scenario_card(scenario)

    # 导出/导入
    if scenarios:
        st.markdown("### 📤 导出/导入")

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="📥 导出场景",
                data=export_scenarios(),
                file_name=f"scenarios_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )

        with col2:
            uploaded = st.file_uploader("📥 导入场景", type=["json"])
            if uploaded:
                data = uploaded.read().decode("utf-8")
                imported, skipped = import_scenarios(data)
                st.success(f"导入 {imported} 个，跳过 {skipped} 个")
                st.rerun()

        if st.button("🗑️ 清空所有场景", type="secondary"):
            clear_all_scenarios()
            st.success("已清空所有场景")
            st.rerun()


def main():
    """主函数"""
    render_header()

    # 模拟器选项卡
    tabs = st.tabs(["🎯 政权实力模拟", "⚔️ 战役模拟", "📅 存续时间推演", "💾 场景管理"])

    with tabs[0]:
        render_power_simulator()

    with tabs[1]:
        render_battle_simulator()

    with tabs[2]:
        render_timeline_simulator()

    with tabs[3]:
        render_scenario_manager()

    st.markdown("---")

    # 使用说明
    with st.expander("📖 使用说明"):
        st.markdown("""
        ### 历史模拟器说明

        **1. 政权实力模拟**
        - 选择你的政权和主要对手
        - 调整实力值和外交关系
        - 查看统一概率和推演结果

        **2. 战役模拟**
        - 设置进攻方和防守方
        - 调整双方实力
        - 添加运气因素模拟不确定性
        - 查看战役结果和置信度

        **3. 存续时间推演**
        - 选择要推演的政权
        - 调整君主能力、经济、军事、外交等因素
        - 查看推演的存续时间变化

        **4. 场景管理**
        - 保存感兴趣的推演场景
        - 导出/导入场景数据
        - 分享你的推演结果
        """)


if __name__ == "__main__":
    main()
