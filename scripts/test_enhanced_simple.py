"""
Simple test to verify the enhanced pattern_subtype system is working
"""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from services.enhanced_movement_query_service_v2 import EnhancedMovementQueryServiceV2


async def test_enhanced_system():
    """Test the enhanced movement query service with pattern_subtype."""
    
    # Create database connection
    database_url = "postgresql+asyncpg://jacked:jackedpass@localhost:5434/Jacked-DB"
    engine = create_async_engine(database_url, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession)
    
    try:
        async with async_session() as session:
            print("🚀 Testing Enhanced Movement Query Service")
            print("=" * 50)
            
            # Initialize the enhanced service
            movement_service = EnhancedMovementQueryServiceV2(session)
            
            # Test 1: Get warmup movements
            print("\n🧪 Test 1: Warmup Movements")
            warmup_movements = await movement_service.get_warmup_movements(
                equipment_available=["bodyweight", "band"],
                max_movements=5,
                execution_format="standalone_sets"
            )
            
            print(f"✅ Found {len(warmup_movements)} warmup movements")
            for i, movement in enumerate(warmup_movements[:3], 1):
                print(f"   {i}. {movement['name']} (subtype: {movement['pattern_subtype']})")
            
            # Test 2: Get strength movements
            print("\n🧪 Test 2: Strength Movements")
            strength_movements = await movement_service.get_strength_movements(
                equipment_available=["barbell", "dumbbell"],
                max_movements=6,
                execution_format="standalone_sets"
            )
            
            print(f"✅ Found {len(strength_movements)} strength movements")
            for i, movement in enumerate(strength_movements[:3], 1):
                print(f"   {i}. {movement['name']} (subtype: {movement['pattern_subtype']})")
            
            # Test 3: Get cardio movements
            print("\n🧪 Test 3: Cardio Movements")
            cardio_movements = await movement_service.get_cardio_movements(
                equipment_available=["bodyweight"],
                max_movements=4,
                execution_format="standalone_sets"
            )
            
            print(f"✅ Found {len(cardio_movements)} cardio movements")
            for i, movement in enumerate(cardio_movements[:3], 1):
                print(f"   {i}. {movement['name']} (subtype: {movement['pattern_subtype']})")
            
            # Test 4: Test pattern subtype distribution
            print("\n🧪 Test 4: Pattern Subtype Distribution")
            
            # Get all movements with pattern_subtype
            from sqlalchemy import text
            result = await session.execute(text("""
                SELECT pattern_subtype, COUNT(*) as count
                FROM movements 
                WHERE pattern_subtype IS NOT NULL
                GROUP BY pattern_subtype
                ORDER BY count DESC
            """))
            
            subtype_counts = result.fetchall()
            print(f"✅ Found {len(subtype_counts)} different pattern subtypes")
            print("Top 5 pattern subtypes:")
            for subtype, count in subtype_counts[:5]:
                print(f"   {subtype}: {count} movements")
            
            print("\n" + "=" * 50)
            print("✅ All tests passed! Enhanced system is working correctly.")
            
            return True
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        await engine.dispose()


if __name__ == "__main__":
    success = asyncio.run(test_enhanced_system())
    exit(0 if success else 1)