"""
五代十国数据 API
使用 FastAPI 提供 RESTful 接口
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import uvicorn

# 导入数据加载模块
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_loader import (
    load_wudai_characters,
    load_fanzhen_complete,
    load_fanzhen_relationships,
)
from src.data_processor import (
    WUDAI_REGIMES,
    SHIGUO_REGIMES,
    REGIME_COLORS,
    process_regime_timeline,
    get_province_regime_mapping,
    get_fanzhen_base_data,
    get_major_events,
    get_yearly_events,
    get_wudai_succession_data,
    get_shiguo_succession_data,
)
from src.config import PROVINCE_MAPPING, FANZHEN_CHRONICLES


# ============================================
# FastAPI 应用
# ============================================

app = FastAPI(
    title="五代十国数据 API",
    description="提供五代十国历史数据的 RESTful 接口",
    version="1.0.0",
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# 数据模型
# ============================================

class Regime(BaseModel):
    name: str
    type: str
    start: int
    end: int
    capital: str
    description: str = ""


class Character(BaseModel):
    name: str
    regime: str
    position: Optional[str]
    start_year: Optional[str]
    end_year: Optional[str]


class Fanzhen(BaseModel):
    name: str
    province: str
    power: int
    area: str


class Event(BaseModel):
    year: int
    event_type: str
    regime: str
    description: str


class Province(BaseModel):
    name: str
    regime: str
    type: str


class APIResponse(BaseModel):
    success: bool
    data: Any
    message: str = ""
    count: Optional[int] = None


# ============================================
# 辅助函数
# ============================================

def dataframe_to_records(df) -> List[Dict]:
    """将 DataFrame 转换为记录列表"""
    if df is None or df.empty:
        return []
    return df.to_dict('records')


# ============================================
# API 接口
# ============================================

@app.get("/", response_model=Dict)
async def root():
    """API 根路径，返回 API 信息"""
    return {
        "name": "五代十国数据 API",
        "version": "1.0.0",
        "description": "提供五代十国历史数据的 RESTful 接口",
        "endpoints": {
            "regimes": "/api/regimes - 获取所有政权",
            "regimes/wudai": "/api/regimes/wudai - 获取五代政权",
            "regimes/shiguo": "/api/regimes/shiguo - 获取十国政权",
            "characters": "/api/characters - 获取人物列表",
            "fanzhen": "/api/fanzhen - 获取藩镇列表",
            "provinces": "/api/provinces - 获取省份映射",
            "events": "/api/events - 获取事件列表",
            "succession": "/api/succession - 获取世系数据",
        }
    }


@app.get("/api/regimes", response_model=APIResponse)
async def get_regimes(
    type: Optional[str] = Query(None, description="政权类型：五代/十国")
):
    """获取所有政权列表"""
    try:
        all_regimes = WUDAI_REGIMES + SHIGUO_REGIMES

        if type:
            if type == "五代":
                all_regimes = WUDAI_REGIMES
            elif type == "十国":
                all_regimes = SHIGUO_REGIMES

        return {
            "success": True,
            "data": all_regimes,
            "count": len(all_regimes)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/regimes/wudai", response_model=APIResponse)
async def get_wudai_regimes():
    """获取五代政权列表"""
    return {
        "success": True,
        "data": WUDAI_REGIMES,
        "count": len(WUDAI_REGIMES)
    }


@app.get("/api/regimes/shiguo", response_model=APIResponse)
async def get_shiguo_regimes():
    """获取十国政权列表"""
    return {
        "success": True,
        "data": SHIGUO_REGIMES,
        "count": len(SHIGUO_REGIMES)
    }


@app.get("/api/regimes/{regime_name}", response_model=APIResponse)
async def get_regime_detail(regime_name: str):
    """获取特定政权详情"""
    all_regimes = WUDAI_REGIMES + SHIGUO_REGIMES

    for regime in all_regimes:
        if regime["name"] == regime_name:
            return {
                "success": True,
                "data": regime,
            }

    raise HTTPException(status_code=404, detail=f"政权 '{regime_name}' 不存在")


@app.get("/api/colors", response_model=APIResponse)
async def get_regime_colors():
    """获取政权颜色映射"""
    return {
        "success": True,
        "data": REGIME_COLORS,
    }


@app.get("/api/characters", response_model=APIResponse)
async def get_characters(
    regime: Optional[str] = Query(None, description="所属政权"),
    limit: int = Query(100, description="返回数量限制")
):
    """获取人物列表"""
    try:
        df = load_wudai_characters()

        if df.empty:
            return {
                "success": True,
                "data": [],
                "count": 0
            }

        if regime:
            df = df[df["regime"] == regime]

        characters = df.head(limit).to_dict('records')

        return {
            "success": True,
            "data": characters,
            "count": len(characters)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/characters/{character_name}", response_model=APIResponse)
async def get_character_detail(character_name: str):
    """获取特定人物详情"""
    try:
        df = load_wudai_characters()

        if df.empty:
            raise HTTPException(status_code=404, detail="人物数据为空")

        character = df[df["name"] == character_name]

        if character.empty:
            raise HTTPException(status_code=404, detail=f"人物 '{character_name}' 不存在")

        return {
            "success": True,
            "data": character.iloc[0].to_dict(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/fanzhen", response_model=APIResponse)
async def get_fanzhen():
    """获取藩镇列表"""
    try:
        fanzhen_data = get_fanzhen_base_data()

        return {
            "success": True,
            "data": fanzhen_data,
            "count": len(fanzhen_data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/fanzhen/{fanzhen_name}", response_model=APIResponse)
async def get_fanzhen_detail(fanzhen_name: str):
    """获取特定藩镇详情"""
    try:
        fanzhen_data = get_fanzhen_base_data()

        if fanzhen_name not in fanzhen_data:
            raise HTTPException(
                status_code=404,
                detail=f"藩镇 '{fanzhen_name}' 不存在"
            )

        # 获取编年史
        chronicles = FANZHEN_CHRONICLES.get(fanzhen_name, [])

        return {
            "success": True,
            "data": {
                "base": fanzhen_data[fanzhen_name],
                "chronicles": chronicles
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/provinces", response_model=APIResponse)
async def get_provinces():
    """获取省份 - 政权映射"""
    try:
        mapping = get_province_regime_mapping()
        provinces = mapping.to_dict('records')

        return {
            "success": True,
            "data": provinces,
            "count": len(provinces)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/province_mapping", response_model=APIResponse)
async def get_province_mapping():
    """获取古今省份名称映射"""
    return {
        "success": True,
        "data": PROVINCE_MAPPING,
    }


@app.get("/api/events", response_model=APIResponse)
async def get_events(
    year: Optional[int] = Query(None, description="特定年份"),
    regime: Optional[str] = Query(None, description="特定政权")
):
    """获取事件列表"""
    try:
        events = get_major_events()

        # 筛选
        if year:
            events = [e for e in events if e.get("year") == year]
        if regime:
            events = [e for e in events if e.get("regime") == regime]

        return {
            "success": True,
            "data": events,
            "count": len(events)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/yearly_events", response_model=APIResponse)
async def get_yearly_events():
    """获取年度事件统计"""
    return {
        "success": True,
        "data": get_yearly_events(),
    }


@app.get("/api/succession", response_model=APIResponse)
async def get_succession(
    regime: Optional[str] = Query(None, description="特定政权")
):
    """获取帝王世系数据"""
    try:
        all_succession = {
            **get_wudai_succession_data(),
            **get_shiguo_succession_data()
        }

        if regime:
            if regime in all_succession:
                return {
                    "success": True,
                    "data": {regime: all_succession[regime]},
                }
            else:
                raise HTTPException(status_code=404, detail=f"政权 '{regime}' 无世系数据")

        return {
            "success": True,
            "data": all_succession,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/timeline", response_model=APIResponse)
async def get_timeline():
    """获取时间线数据"""
    try:
        df = process_regime_timeline()
        return {
            "success": True,
            "data": df.to_dict('records'),
            "count": len(df)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats", response_model=APIResponse)
async def get_stats():
    """获取统计数据"""
    try:
        all_regimes = WUDAI_REGIMES + SHIGUO_REGIMES

        stats = {
            "total_regimes": len(all_regimes),
            "wudai_count": len(WUDAI_REGIMES),
            "shiguo_count": len(SHIGUO_REGIMES),
            "total_years": max(r["end"] for r in all_regimes) - min(r["start"] for r in all_regimes),
            "avg_duration": sum(r["end"] - r["start"] for r in all_regimes) / len(all_regimes),
        }

        return {
            "success": True,
            "data": stats,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# 错误处理
# ============================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "success": False,
        "error": "Not Found",
        "detail": str(exc)
    }


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {
        "success": False,
        "error": "Internal Server Error",
        "detail": str(exc)
    }


# ============================================
# 启动入口
# ============================================

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
