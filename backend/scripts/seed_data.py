"""
Seed initial product and stats data.
Run from backend/ directory:
    conda activate ai-full-stack
    python -m scripts.seed_data
"""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings
from app.models.domain.product import (
    Product, ProductFeature, ProductSpec, ProductImage, SiteStat
)


async def seed(session: AsyncSession) -> None:
    from sqlalchemy import select, func
    count = (await session.execute(select(func.count()).select_from(Product))).scalar()
    if count and count > 0:
        print(f"Already seeded ({count} products found). Skipping.")
        return

    # ── Site Stats ───────────────────────────────────────────
    session.add_all([
        SiteStat(label="核心专利",  value="200+", unit="项", sort_order=0),
        SiteStat(label="研发工程师", value="50+",  unit="人", sort_order=1),
        SiteStat(label="合作伙伴",  value="30+",  unit="家", sort_order=2),
    ])

    # ── AI眼镜 ───────────────────────────────────────────────
    glasses = Product(
        slug="ai-glasses", category="glasses", name="AI眼镜",
        tagline="实时感知，智能随行",
        description="融合毫米波雷达与边缘计算的新一代AR智能眼镜，实现环境实时感知与信息叠加显示。",
        cover_image="/static/products/glasses-cover.webp", sort_order=0,
    )
    glasses.features = [
        ProductFeature(icon="eye",    title="AR叠加显示", description="低延迟透视显示，信息无缝融入现实", sort_order=0),
        ProductFeature(icon="cpu",    title="端侧AI推理", description="NPU本地运行，保护数据隐私",         sort_order=1),
        ProductFeature(icon="signal", title="毫米波感知", description="精准识别距离与姿态",               sort_order=2),
    ]
    glasses.specs = [
        ProductSpec(spec_key="重量",   spec_value="42g",            sort_order=0),
        ProductSpec(spec_key="续航",   spec_value="8小时",          sort_order=1),
        ProductSpec(spec_key="显示",   spec_value="1080p双目",      sort_order=2),
        ProductSpec(spec_key="处理器", spec_value="自研NPU",        sort_order=3),
        ProductSpec(spec_key="连接",   spec_value="BT5.3 / WiFi 6", sort_order=4),
    ]
    glasses.images = [
        ProductImage(image_url="/static/products/glasses-1.webp", alt_text="AI眼镜正面", sort_order=0),
        ProductImage(image_url="/static/products/glasses-2.webp", alt_text="AI眼镜侧面", sort_order=1),
    ]
    session.add(glasses)

    # ── AI机器人 ─────────────────────────────────────────────
    robot = Product(
        slug="ai-robot", category="robot", name="AI机器人",
        tagline="智能陪伴，情感连接",
        description="搭载大语言模型的家用智能陪伴机器人，具备多模态理解与自然对话能力。",
        cover_image="/static/products/robot-cover.webp", sort_order=1,
    )
    robot.features = [
        ProductFeature(icon="brain",  title="LLM对话",  description="自然语言理解，上下文记忆", sort_order=0),
        ProductFeature(icon="camera", title="视觉感知",  description="人脸识别与情绪分析",       sort_order=1),
        ProductFeature(icon="move",   title="自主移动",  description="激光SLAM导航，避障巡逻",   sort_order=2),
    ]
    robot.specs = [
        ProductSpec(spec_key="身高",   spec_value="35cm",        sort_order=0),
        ProductSpec(spec_key="续航",   spec_value="6小时",       sort_order=1),
        ProductSpec(spec_key="处理器", spec_value="骁龙8 Gen2",  sort_order=2),
        ProductSpec(spec_key="传感器", spec_value="ToF+RGB双摄", sort_order=3),
    ]
    robot.images = [
        ProductImage(image_url="/static/products/robot-1.webp", alt_text="AI机器人正面", sort_order=0),
    ]
    session.add(robot)

    # ── AI玩具 ──────────────────────────────────────────────
    toy = Product(
        slug="ai-toy", category="toy", name="AI玩具",
        tagline="启蒙智慧，伴随成长",
        description="面向3-12岁儿童的AI教育玩具，通过互动故事与益智游戏激发创造力。",
        cover_image="/static/products/toy-cover.webp", sort_order=2,
    )
    toy.features = [
        ProductFeature(icon="book", title="自适应课程", description="根据孩子水平动态调整内容", sort_order=0),
        ProductFeature(icon="mic",  title="语音交互",   description="中英双语，自然对话",       sort_order=1),
        ProductFeature(icon="safe", title="儿童安全",   description="无蓝光屏幕，离线优先",     sort_order=2),
    ]
    toy.specs = [
        ProductSpec(spec_key="适龄", spec_value="3-12岁", sort_order=0),
        ProductSpec(spec_key="续航", spec_value="10小时", sort_order=1),
        ProductSpec(spec_key="存储", spec_value="16GB",   sort_order=2),
    ]
    toy.images = [
        ProductImage(image_url="/static/products/toy-1.webp", alt_text="AI玩具正面", sort_order=0),
    ]
    session.add(toy)

    await session.commit()
    print("✓ Seed data inserted: 3 products, 3 site stats")


async def main() -> None:
    engine = create_async_engine(settings.DATABASE_URL)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        await seed(session)
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
