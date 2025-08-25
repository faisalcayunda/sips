"""
Test cases for ArticleService.
"""

from unittest.mock import AsyncMock, Mock

import pytest

from app.models import ArticleModel
from app.repositories import ArticleRepository
from app.schemas import UserSchema
from app.services import ArticleService


class TestArticleService:
    """Test cases for ArticleService."""

    @pytest.fixture
    def mock_article_repository(self):
        """Mock ArticleRepository."""
        repository = Mock(spec=ArticleRepository)
        repository.create = AsyncMock()
        repository.update = AsyncMock()
        return repository

    @pytest.fixture
    def mock_user(self):
        """Mock UserSchema."""
        user = Mock(spec=UserSchema)
        user.id = "user_123"
        return user

    @pytest.fixture
    def article_service(self, mock_article_repository):
        """Create ArticleService instance with mocked repository."""
        return ArticleService(repository=mock_article_repository)

    @pytest.fixture
    def sample_article_data(self):
        """Sample article data for testing."""
        return {
            "title": "Test Article Title",
            "content": "This is test article content",
            "enable": "Y",
            "cover": "test-cover.jpg",
        }

    @pytest.fixture
    def sample_article_model(self):
        """Sample ArticleModel instance."""
        article = Mock(spec=ArticleModel)
        article.id = 1
        article.title = "Test Article Title"
        article.slug = "test-article-title"
        article.content = "This is test article content"
        article.enable = "Y"
        article.cover = "test-cover.jpg"
        article.created_by = "user_123"
        article.updated_by = None
        return article

    def test_slugify_normal_text(self, article_service):
        """Test _slugify method with normal text."""
        result = article_service._slugify("Hello World")
        assert result == "hello-world"

    def test_slugify_with_multiple_spaces(self, article_service):
        """Test _slugify method with multiple spaces."""
        result = article_service._slugify("  Multiple   Spaces  ")
        assert result == "multiple---spaces"

    def test_slugify_with_special_characters(self, article_service):
        """Test _slugify method with special characters."""
        result = article_service._slugify("Special!@#$%^&*()Characters")
        assert result == "special!@#$%^&*()characters"

    def test_slugify_empty_string(self, article_service):
        """Test _slugify method with empty string."""
        result = article_service._slugify("")
        assert result == ""

    def test_slugify_single_word(self, article_service):
        """Test _slugify method with single word."""
        result = article_service._slugify("Article")
        assert result == "article"

    @pytest.mark.asyncio
    async def test_create_with_title(self, article_service, mock_article_repository, mock_user, sample_article_data):
        """Test create method with title field."""
        # Arrange
        expected_article = Mock(spec=ArticleModel)
        expected_article.id = 1
        expected_article.title = "Test Article Title"
        expected_article.slug = "test-article-title"
        expected_article.created_by = "user_123"

        mock_article_repository.create.return_value = expected_article

        # Act
        result = await article_service.create(sample_article_data, mock_user)

        # Assert
        assert result == expected_article
        mock_article_repository.create.assert_called_once()

        # Verify the data passed to repository.create
        call_args = mock_article_repository.create.call_args[0][0]
        assert call_args["title"] == "Test Article Title"
        assert call_args["slug"] == "test-article-title"
        assert call_args["created_by"] == "user_123"

    @pytest.mark.asyncio
    async def test_create_without_title_raises_error(self, article_service, mock_article_repository, mock_user):
        """Test create method without title field raises KeyError."""
        # Arrange
        data_without_title = {"content": "This is test article content", "enable": "Y"}

        # Act & Assert
        with pytest.raises(KeyError, match="title"):
            await article_service.create(data_without_title, mock_user)

        # Verify repository.create was not called
        mock_article_repository.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_with_title(self, article_service, mock_article_repository, mock_user):
        """Test update method with title field."""
        # Arrange
        article_id = "1"
        update_data = {"title": "Updated Article Title", "content": "Updated content"}

        expected_article = Mock(spec=ArticleModel)
        expected_article.id = 1
        expected_article.title = "Updated Article Title"
        expected_article.slug = "updated-article-title"
        expected_article.updated_by = "user_123"

        mock_article_repository.update.return_value = expected_article

        # Act
        result = await article_service.update(article_id, update_data, mock_user)

        # Assert
        assert result == expected_article
        mock_article_repository.update.assert_called_once_with(article_id, update_data, refresh=True)

        # Verify the data passed to repository.update
        call_args = mock_article_repository.update.call_args[0][1]
        assert call_args["title"] == "Updated Article Title"
        assert call_args["slug"] == "updated-article-title"
        assert call_args["updated_by"] == "user_123"

    @pytest.mark.asyncio
    async def test_update_without_title(self, article_service, mock_article_repository, mock_user):
        """Test update method without title field."""
        # Arrange
        article_id = "1"
        update_data = {"content": "Updated content only"}

        expected_article = Mock(spec=ArticleModel)
        mock_article_repository.update.return_value = expected_article

        # Act
        result = await article_service.update(article_id, update_data, mock_user)

        # Assert
        assert result == expected_article
        mock_article_repository.update.assert_called_once_with(article_id, update_data, refresh=True)

        # Verify the data passed to repository.update
        call_args = mock_article_repository.update.call_args[0][1]
        assert call_args["updated_by"] == "user_123"
        assert "slug" not in call_args

    @pytest.mark.asyncio
    async def test_update_with_refresh_false(self, article_service, mock_article_repository, mock_user):
        """Test update method with refresh=False."""
        # Arrange
        article_id = "1"
        update_data = {"title": "Updated Title"}

        expected_article = Mock(spec=ArticleModel)
        mock_article_repository.update.return_value = expected_article

        # Act
        result = await article_service.update(article_id, update_data, mock_user, refresh=False)

        # Assert
        assert result == expected_article
        mock_article_repository.update.assert_called_once_with(article_id, update_data, refresh=False)

    @pytest.mark.asyncio
    async def test_update_with_complex_title(self, article_service, mock_article_repository, mock_user):
        """Test update method with complex title containing special characters."""
        # Arrange
        article_id = "1"
        update_data = {"title": "Complex Title with Numbers 123 & Special @#$%", "content": "Updated content"}

        expected_article = Mock(spec=ArticleModel)
        mock_article_repository.update.return_value = expected_article

        # Act
        result = await article_service.update(article_id, update_data, mock_user)

        # Assert
        assert result == expected_article

        # Verify the slug generation
        call_args = mock_article_repository.update.call_args[0][1]
        assert call_args["slug"] == "complex-title-with-numbers-123-&-special-@#$%"

    @pytest.mark.asyncio
    async def test_create_and_update_integration(self, article_service, mock_article_repository, mock_user):
        """Test create and update methods work together correctly."""
        # Arrange - Create
        create_data = {"title": "Initial Title", "content": "Initial content", "enable": "Y"}

        created_article = Mock(spec=ArticleModel)
        created_article.id = 1
        created_article.title = "Initial Title"
        created_article.slug = "initial-title"
        created_article.created_by = "user_123"

        mock_article_repository.create.return_value = created_article

        # Act - Create
        result_create = await article_service.create(create_data, mock_user)

        # Assert - Create
        assert result_create == created_article
        assert mock_article_repository.create.call_count == 1

        # Arrange - Update
        update_data = {"title": "Updated Title"}

        updated_article = Mock(spec=ArticleModel)
        updated_article.id = 1
        updated_article.title = "Updated Title"
        updated_article.slug = "updated-title"
        updated_article.updated_by = "user_123"

        mock_article_repository.update.return_value = updated_article

        # Act - Update
        result_update = await article_service.update("1", update_data, mock_user)

        # Assert - Update
        assert result_update == updated_article
        assert mock_article_repository.update.call_count == 1

    def test_slugify_edge_cases(self, article_service):
        """Test _slugify method with edge cases."""
        # Test with numbers
        assert article_service._slugify("Article 123") == "article-123"

        # Test with mixed case
        assert article_service._slugify("MiXeD cAsE") == "mixed-case"

        # Test with leading/trailing spaces
        assert article_service._slugify("  Leading Spaces  ") == "leading-spaces"

        # Test with single character
        assert article_service._slugify("A") == "a"

        # Test with only spaces
        assert article_service._slugify("   ") == ""
