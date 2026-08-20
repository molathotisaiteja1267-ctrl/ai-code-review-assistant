from typing import List, Dict, Any, Optional

class GitHubService:
    @staticmethod
    def get_demo_repositories() -> List[Dict[str, Any]]:
        return [
            {
                "id": 101,
                "name": "ecommerce-api",
                "full_name": "acme-corp/ecommerce-api",
                "owner": "acme-corp",
                "default_branch": "main",
                "is_private": False,
                "description": "Core microservices API for payments, checkout, and inventory."
            },
            {
                "id": 102,
                "name": "data-pipeline",
                "full_name": "acme-corp/data-pipeline",
                "owner": "acme-corp",
                "default_branch": "main",
                "is_private": True,
                "description": "ETL ingestion and analytics pipeline."
            },
            {
                "id": 103,
                "name": "auth-service",
                "full_name": "acme-corp/auth-service",
                "owner": "acme-corp",
                "default_branch": "main",
                "is_private": False,
                "description": "OAuth2 / JWT authentication and user management."
            }
        ]

    @staticmethod
    def get_demo_pull_requests(repo_full_name: str) -> List[Dict[str, Any]]:
        if "ecommerce" in repo_full_name:
            return [
                {
                    "id": 201,
                    "number": 42,
                    "title": "feat: Add user order lookup with search filtering",
                    "description": "Adds direct SQL search filter by customer username and order ID.",
                    "state": "open",
                    "base_branch": "main",
                    "head_branch": "feat/order-lookup",
                    "author": "dev-alex",
                    "changed_files_count": 2,
                    "additions": 35,
                    "deletions": 4,
                    "diff_content": "diff --git a/app/routes/orders.py b/app/routes/orders.py\n--- a/app/routes/orders.py\n+++ b/app/routes/orders.py\n@@ -14,6 +14,20 @@ def get_order_by_id(order_id):\n+def search_customer_orders(customer_id, filter_query):\n+    conn = db.get_connection()\n+    cursor = conn.cursor()\n+    # Direct query string concatenation\n+    sql = f\"SELECT * FROM orders WHERE customer_id = '{customer_id}' AND status = '{filter_query}'\"\n+    cursor.execute(sql)\n+    return cursor.fetchall()\n"
                },
                {
                    "id": 202,
                    "number": 45,
                    "title": "perf: Batch calculate cart discounts for multi-item checkout",
                    "description": "Iterates over cart items to calculate discount multipliers.",
                    "state": "open",
                    "base_branch": "main",
                    "head_branch": "perf/discount-calc",
                    "author": "sde-sarah",
                    "changed_files_count": 1,
                    "additions": 22,
                    "deletions": 8,
                    "diff_content": "diff --git a/app/services/pricing.py b/app/services/pricing.py\n--- a/app/services/pricing.py\n+++ b/app/services/pricing.py\n@@ -30,6 +30,16 @@ def calculate_total(cart):\n+def apply_promotions(cart_items, promo_rules):\n+    final_prices = []\n+    for item in cart_items:\n+        for rule in promo_rules:\n+            for tier in rule.get('tiers', []):\n+                if tier['sku'] == item['sku']:\n+                    item['discount'] = tier['discount_pct']\n+        final_prices.append(item)\n+    return final_prices\n"
                }
            ]
        elif "auth" in repo_full_name:
            return [
                {
                    "id": 301,
                    "number": 12,
                    "title": "fix: Hardcoded master key fallback for local auth testing",
                    "description": "Sets static fallback JWT secret for easier local Docker compose development.",
                    "state": "open",
                    "base_branch": "main",
                    "head_branch": "fix/jwt-fallback",
                    "author": "backend-john",
                    "changed_files_count": 1,
                    "additions": 14,
                    "deletions": 2,
                    "diff_content": "diff --git a/app/auth/tokens.py b/app/auth/tokens.py\n--- a/app/auth/tokens.py\n+++ b/app/auth/tokens.py\n@@ -8,4 +8,12 @@ import jwt\n+JWT_SECRET_KEY = \"SUPER_SECRET_PRODUCTION_MASTER_KEY_2026_DO_NOT_SHARE\"\n+\ndef decode_token_unsafe(token):\n+    try:\n+        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[\"HS256\"])\n+    except:\n+        pass\n"
                }
            ]
        else:
            return [
                {
                    "id": 401,
                    "number": 7,
                    "title": "refactor: Clean up data transformer and add docstrings",
                    "description": "Standard refactor with parameterized queries and proper logging.",
                    "state": "open",
                    "base_branch": "main",
                    "head_branch": "refactor/clean-pipeline",
                    "author": "lead-emma",
                    "changed_files_count": 1,
                    "additions": 20,
                    "deletions": 15,
                    "diff_content": "diff --git a/pipeline/transform.py b/pipeline/transform.py\n--- a/pipeline/transform.py\n+++ b/pipeline/transform.py\n@@ -10,12 +10,18 @@ import logging\n+logger = logging.getLogger(__name__)\n+\ndef sanitize_record(record: dict) -> dict:\n+    return {k: str(v).strip() for k, v in record.items() if v is not None}\n"
                }
            ]
